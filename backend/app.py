from flask import Flask, jsonify
from routes.track_number import track_number_bp
from routes.report_number import report_number_bp
from models.database import engine, Base
from flask_cors import CORS
from models.database import DATABASE_URL
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models.database import SessionLocal
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Register blueprints
app.register_blueprint(track_number_bp)
app.register_blueprint(report_number_bp)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SessionLocal()

# User model for Flask-Login
class UserModel(UserMixin, User):
    pass

@login_manager.user_loader
def load_user(user_id):
    return db.query(User).get(user_id)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))

        # Check if the user already exists
        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.add(new_user)
        db.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify the user exists
        user = db.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Logout endpoint
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/report')
@login_required
def report():
    return render_template('report.html')


# Initialize tables
Base.metadata.create_all(bind=engine)

# Enable CORS
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Tafuta API!"})

if __name__ == "__main__":
    print("Starting Flask app...")  # Log to confirm script is executing
    app.run(debug=True)

from models.database import Base, engine

print("Initializing database...")
Base.metadata.create_all(bind=engine)
print("Database initialized!")
