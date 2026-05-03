from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Task, User
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    # On every protected page -> check session.get('user_id') manually at top of route
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    # Read: Fetch all tasks for the logged in user
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    
    return render_template('dashboard.html', tasks=tasks)

@main_bp.route('/task/new', methods=['GET', 'POST'])
def new_task():
    # Protected route manual check
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'Pending')
        
        # Validation
        if not title:
            flash('Task title is required.', 'danger')
            return redirect(url_for('main.new_task'))
            
        # Create: Add new task
        task = Task(title=title, description=description, status=status, user_id=session.get('user_id'))
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('task_form.html', task=None, title="New Task")

@main_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    # Protected route manual check
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
        
    # Get task and ensure it belongs to the current user
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get('user_id'):
        flash('You are not authorized to edit this task.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'Pending')
        
        if not title:
            flash('Task title is required.', 'danger')
            return redirect(url_for('main.edit_task', task_id=task.id))
            
        # Update: Modify existing task properties
        task.title = title
        task.description = description
        task.status = status
        db.session.commit()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('task_form.html', task=task, title="Edit Task")

@main_bp.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    # Protected route manual check
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
        
    # Get task and ensure it belongs to the current user
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get('user_id'):
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    # Delete: Remove task from database
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))
