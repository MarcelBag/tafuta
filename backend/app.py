from flask import Flask, jsonify, redirect, url_for, render_template, request, flash
from routes.track_number import track_number_bp
from routes.report_number import report_number_bp
from models.database import engine, Base, SessionLocal
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(track_number_bp)
app.register_blueprint(report_number_bp)

# Database session
db = SessionLocal()

# User model for Flask-Login
class UserModel(UserMixin, User):
    pass

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return db.query(User).get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint."""
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        company = request.form.get('company')
        email = request.form.get('username')
        password = request.form.get('password')

        # Validate input
        if not name or not surname or not company or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        # Check if the user already exists
        existing_user = db.query(User).filter_by(username=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(
            name=name,
            surname=surname,
            company=company,
            username=email,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Verify the user exists
        user = db.query(User).filter_by(username=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout endpoint."""
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard view."""
    return render_template('dashboard.html')

@app.route('/report')
@login_required
def report():
    """Reports view."""
    return render_template('report.html')

@app.route('/')
def home():
    """Home endpoint."""
    return jsonify({"message": "Welcome to Tafuta API!"})

# Initialize database tables
print("Initializing database...")
Base.metadata.create_all(bind=engine)
print("Database initialized!")

if __name__ == "__main__":
    print("Starting Flask app...")  # Log to confirm script execution
    app.run(debug=True)
