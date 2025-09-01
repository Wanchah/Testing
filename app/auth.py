"""
EduMorph Authentication Blueprint
User authentication, registration, and profile management.

This module handles:
- User login and logout
- User registration with role selection
- Password management
- User profile updates
- Age-appropriate content access
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, UserRole, AgeGroup, db
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page with age-adaptive interface.
    Supports all user roles: students, teachers, parents, admins.
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return render_template('auth/login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password):
            if user.is_active:
                login_user(user, remember=remember)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Redirect based on user role
                if user.role == UserRole.TEACHER:
                    flash(f'Welcome back, {user.get_full_name()}! Ready to inspire minds?', 'success')
                    return redirect(url_for('dashboard.teacher_dashboard'))
                elif user.role == UserRole.STUDENT:
                    flash(f'Welcome back, {user.get_full_name()}! Ready to learn something amazing?', 'success')
                    return redirect(url_for('dashboard.student_dashboard'))
                elif user.role == UserRole.PARENT:
                    flash(f'Welcome back, {user.get_full_name()}! Monitor your child\'s progress.', 'success')
                    return redirect(url_for('dashboard.parent_dashboard'))
                else:
                    flash(f'Welcome back, {user.get_full_name()}!', 'success')
                    return redirect(url_for('main.index'))
            else:
                flash('Account is deactivated. Please contact support.', 'error')
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User registration page with role and age group selection.
    Creates appropriate user accounts for different learning needs.
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        role = request.form.get('role', 'student')
        age_group = request.form.get('age_group', 'teens')
        date_of_birth = request.form.get('date_of_birth', '')
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Please provide a valid email address.')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if not first_name or not last_name:
            errors.append('Please provide both first and last names.')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists. Please choose another.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered. Please use another email or login.')
        
        # Validate role and age group combinations
        if role == 'teacher' and age_group == 'children':
            errors.append('Teachers cannot be registered as children. Please select appropriate age group.')
        
        if role == 'parent' and age_group in ['children', 'teens']:
            errors.append('Parents should be adults. Please select appropriate age group.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/signup.html')
        
        try:
            # Create new user
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=UserRole(role),
                age_group=AgeGroup(age_group),
                date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None
            )
            user.set_password(password)
            
            # Set default preferences based on age group
            if age_group == 'children':
                user.theme_preference = 'colorful'
                user.font_size = 'large'
                user.accessibility_features = {'high_contrast': True, 'simple_navigation': True}
            elif age_group == 'teens':
                user.theme_preference = 'modern'
                user.font_size = 'medium'
                user.accessibility_features = {'gamification': True}
            else:
                user.theme_preference = 'professional'
                user.font_size = 'medium'
                user.accessibility_features = {}
            
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! Please login to continue.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
            return render_template('auth/signup.html')
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout functionality."""
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """
    User profile page with age-adaptive interface.
    Shows user information and learning preferences.
    """
    
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Edit user profile with role-appropriate options.
    Allows users to update preferences and personal information.
    """
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        bio = request.form.get('bio', '').strip()
        theme_preference = request.form.get('theme_preference', 'default')
        font_size = request.form.get('font_size', 'medium')
        high_contrast = request.form.get('high_contrast', False) == 'on'
        
        # Validation
        if not first_name or not last_name:
            flash('Please provide both first and last names.', 'error')
            return render_template('auth/edit_profile.html', user=current_user)
        
        try:
            # Update user profile
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.bio = bio
            current_user.theme_preference = theme_preference
            current_user.font_size = font_size
            current_user.high_contrast = high_contrast
            
            # Update accessibility features
            current_user.accessibility_features.update({
                'high_contrast': high_contrast,
                'font_size': font_size
            })
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
    
    return render_template('auth/edit_profile.html', user=current_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Change password functionality with security validation.
    """
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not current_password or not new_password or not confirm_password:
            flash('Please fill in all password fields.', 'error')
            return render_template('auth/change_password.html')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long.', 'error')
            return render_template('auth/change_password.html')
        
        try:
            # Update password
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error changing password: {str(e)}', 'error')
    
    return render_template('auth/change_password.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Forgot password functionality (placeholder for email integration).
    """
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Please provide your email address.', 'error')
            return render_template('auth/forgot_password.html')
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # TODO: Implement email password reset functionality
            flash('Password reset instructions have been sent to your email.', 'info')
        else:
            flash('No account found with that email address.', 'error')
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/api/user-info')
@login_required
def api_user_info():
    """
    API endpoint for user information.
    Used by frontend for personalization and UI adaptation.
    """
    
    user_info = {
        'id': current_user.id,
        'username': current_user.username,
        'full_name': current_user.get_full_name(),
        'role': current_user.role.value,
        'age_group': current_user.age_group.value,
        'theme_preference': current_user.theme_preference,
        'font_size': current_user.font_size,
        'high_contrast': current_user.high_contrast,
        'accessibility_features': current_user.accessibility_features
    }
    
    return jsonify({'success': True, 'user': user_info})

@auth_bp.route('/api/validate-username/<username>')
def api_validate_username(username):
    """
    API endpoint for username validation during registration.
    """
    
    if len(username) < 3:
        return jsonify({'valid': False, 'message': 'Username must be at least 3 characters long.'})
    
    if User.query.filter_by(username=username).first():
        return jsonify({'valid': False, 'message': 'Username already exists.'})
    
    return jsonify({'valid': True, 'message': 'Username is available.'})

@auth_bp.route('/api/validate-email/<email>')
def api_validate_email(email):
    """
    API endpoint for email validation during registration.
    """
    
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return jsonify({'valid': False, 'message': 'Please provide a valid email address.'})
    
    if User.query.filter_by(email=email).first():
        return jsonify({'valid': False, 'message': 'Email already registered.'})
    
    return jsonify({'valid': True, 'message': 'Email is available.'})
