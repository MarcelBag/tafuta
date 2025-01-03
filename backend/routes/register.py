from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import SessionLocal
from models.user import User
from werkzeug.security import generate_password_hash

# Blueprint for registration
register_bp = Blueprint('register', __name__)

db = SessionLocal()

@register_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('register.register'))

        # Check if the user already exists
        existing_user = db.query(User).filter_by(username=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register.register'))

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
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
        return redirect(url_for('login.login'))
    return render_template('register.html')
