from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, current_user
from routes.track_number import track_number_bp
from routes.report_number import report_number_bp
from routes.login import login_bp
from routes.register import register_bp
from models.database import Base, engine, SessionLocal
from models.user import User
import os

# Flask app initialization
app = Flask(
    __name__,
    template_folder='templates',  # Path to the templates folder
    static_folder='../static'     # Path to the static files folder
)

app.secret_key = 'your_secret_key'

# Initialize Flask-Login
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
    return render_template('index.html')

# Enable CORS for cross-origin requests
CORS(app)

# Register blueprints for modular routing
app.register_blueprint(track_number_bp)
app.register_blueprint(report_number_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)


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

# Initialize database tables
print("Initializing database...")
Base.metadata.create_all(bind=engine)
print("Database initialized!")

if __name__ == "__main__":
    print("Starting Flask app...")  # Log for debugging
    app.run(debug=True, port=5000)  # Flask will run on http://127.0.0.1:5000/
