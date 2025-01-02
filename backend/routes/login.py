from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.database import SessionLocal
from models.user import User
from werkzeug.security import check_password_hash

# Blueprint for login
login_bp = Blueprint('login', __name__)

db = SessionLocal()

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Verify the user exists
        user = db.query(User).filter_by(username=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login.login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@login_bp.route('/logout')
@login_required
def logout():
    """User logout endpoint."""
    logout_user()
    return redirect(url_for('login.login'))
