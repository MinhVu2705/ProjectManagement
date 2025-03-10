from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_mail import Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import current_app as app
from datetime import datetime, timedelta
import plotly.graph_objs as go

from . import db, bcrypt, mail, cache
from .models import User, Project, Task, Role
from .utils import admin_required
import logging
from flask_login import login_required
from flask import make_response, jsonify
import json
from flask import request


# ----------------------------
# Home and Authentication Routes
# ----------------------------

@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user_role = Role.query.filter_by(name='User').first()  # Default role: User
        user = User(username=username, email=email, password=password, role_id=user_role.id)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.name
            }
            response = make_response(redirect(url_for('home')))
            response.set_cookie('user', jsonify(user_data).get_data(as_text=True))
            flash('Logged in successfully!', 'success')
            return response
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html')


# ----------------------------
# Project Routes
# ----------------------------

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
@admin_required
def create_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects'))
    return render_template('create_project.html')


@app.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects'))
    return render_template('edit_project.html', project=project)


@app.route('/projects/delete/<int:project_id>', methods=['POST'])
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects'))


# ----------------------------
# Task Routes
# ----------------------------

@app.route('/tasks/<int:project_id>')
def tasks(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    if not current_user.is_admin():  # If User, only show assigned tasks
        tasks = [task for task in tasks if task.assigned_to == current_user.id]
    return render_template('tasks.html', tasks=tasks, project_id=project_id)


@app.route('/tasks/new/<int:project_id>', methods=['GET', 'POST'])
def create_task(project_id):
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        assigned_to = request.form.get('assigned_to')  # Assign task to user
        task = Task(name=name, description=description, project_id=project_id, deadline=deadline, assigned_to=assigned_to)
        db.session.add(task)
        db.session.commit()

        # Send notification email
        user = User.query.get(assigned_to)
        if user:
            msg = Message(
                subject=f'New Task Assigned: {name}',
                recipients=[user.email],
                body=f'Hello {user.username},\n\nYou have been assigned a new task:\n\n'
                     f'Task Name: {name}\nDescription: {description}\nDeadline: {deadline}\n\n'
                     f'Best regards,\nProject Management System'
            )
            mail.send(msg)

        flash('Task created successfully and notification sent!', 'success')
        return redirect(url_for('tasks', project_id=project_id))
    users = User.query.all()  # Fetch users for assignment
    return render_template('create_task.html', project_id=project_id, users=users)


@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.name = request.form.get('name')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks', project_id=task.project_id))
    return render_template('edit_task.html', task=task)


@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks', project_id=project_id))


# ----------------------------
# Statistics Routes
# ----------------------------

@app.route('/stats')
@cache.cached(timeout=60)  # Cache for 60 seconds
def stats():
    projects = Project.query.all()
    project_names = [project.name for project in projects]
    project_progress = []

    for project in projects:
        total_tasks = Task.query.filter_by(project_id=project.id).count()
        completed_tasks = Task.query.filter_by(project_id=project.id, status='Completed').count()
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        project_progress.append(progress)

    # Create bar chart using Plotly
    fig = go.Figure([go.Bar(x=project_names, y=project_progress)])
    fig.update_layout(title='Project Progress',
                      xaxis=dict(title='Projects'),
                      yaxis=dict(title='Completion Percentage'))

    return render_template('stats.html', graph_html=fig.to_html(full_html=False))


@app.route('/task-stats')
def task_stats():
    statuses = ['Not Started', 'In Progress', 'Completed']
    counts = [Task.query.filter_by(status=status).count() for status in statuses]

    # Create pie chart using Plotly
    fig = go.Figure([go.Pie(labels=statuses, values=counts)])
    fig.update_layout(title='Task Status Distribution')

    return render_template('task_stats.html', graph_html=fig.to_html(full_html=False))


# ----------------------------
# Scheduler and Role Initialization
# ----------------------------

def send_deadline_reminders():
    tasks = Task.query.all()
    for task in tasks:
        if task.deadline and task.status != 'Completed':
            days_left = (task.deadline - datetime.utcnow().date()).days
            if 0 < days_left <= 2:  # Notify if task is due in 1-2 days
                user = User.query.get(task.assigned_to)
                if user:
                    msg = Message(
                        subject=f'Reminder: Task Deadline Approaching',
                        recipients=[user.email],
                        body=f'Hello {user.username},\n\n'
                             f'This is a reminder that the task "{task.name}" is due on {task.deadline}.\n\n'
                             f'Best regards,\nProject Management System'
                    )
                    mail.send(msg)


def create_roles():
    if Role.query.count() == 0:
        db.session.add_all([Role(name='Admin'), Role(name='User')])
        db.session.commit()

# Thêm vào trong create_app hoặc một nơi khởi tạo ứng dụng
with app.app_context():
    create_roles()