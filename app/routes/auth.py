from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app import db
import hashlib
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Manual Form Validation
        if not name or not email or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.signup'))
            
        # Basic email format validation
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('auth.signup'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.signup'))
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('auth.signup'))
            
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists.', 'warning')
            return redirect(url_for('auth.signup'))
            
        # Manually hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create new user
        new_user = User(name=name, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Manual Form Validation
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return redirect(url_for('auth.login'))
            
        # Manually hash input password to compare with DB
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Query DB
        user = User.query.filter_by(email=email).first()
        
        # Compare hashes manually
        if user and user.password == hashed_input_password:
            # On success -> manage session manually
            session['user_id'] = user.id
            session['username'] = user.name
            
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Please check your login details and try again.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Logout by manually clearing the session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
