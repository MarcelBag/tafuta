from flask import Flask, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user
from routes.track_number import track_number_bp
from routes.report_number import report_number_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.track_map import track_map_bp
from models.database import Base, engine, SessionLocal
from models.user import User
from routes.location_routes import location_bp
import os

# Flask app initialization
app = Flask(
    __name__,
    #templates source
    template_folder='templates',  
     # static folders 
    static_folder='../static'    
)

app.secret_key = 'your_secret_key'

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

# User loader function for Flask-Login
db = SessionLocal()

@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID."""
    return db.query(User).get(user_id)

@app.route('/')
def home():
    """Render the home page."""
    print(f"Current user: {current_user.is_authenticated}")  # Debugging log
    return render_template('index.html')

# Ebaling CORS only for API routes that need it
CORS(track_number_bp)
CORS(report_number_bp)
CORS(track_map_bp)

# Registering blueprints for modular routing
app.register_blueprint(track_number_bp)
app.register_blueprint(report_number_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(track_map_bp)
app.register_blueprint(location_bp)

@app.route('/tracking')
@login_required
def tracking():
    """Render the tracking page."""
    return render_template('track.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')

@app.route('/report')
@login_required
def report():
    """Render the report page."""
    return render_template('report.html')

@app.route('/logout')
@login_required
def logout():
    """Log out the current user and redirect to the home page."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Initializing database tables
print("Initializing database...")
Base.metadata.create_all(bind=engine)
print("Database initialized!")

if __name__ == "__main__":
     # debugging log
    print("Starting Flask app...") 
    # runing on port 5 http://127.0.0.1:5000/
    app.run(debug=True, port=5000)  
