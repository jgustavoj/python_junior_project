from flask import Blueprint, flash, redirect, render_template, url_for, request
from .models import Todo, User
from flask_login import login_required, current_user
from . import db
import datetime as dt


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('login.html', user=current_user)

"""
Contacts Views
"""

@views.route('/contacts')
def all_contacts():
    return render_template('contacts.html', user=current_user)


"""
To-do Views
"""

# All task with user route
@views.route('/todos')
@login_required
def all_todos():
    if current_user.is_authenticated:
        complete_task = Todo.query.filter_by(complete=True).all()
        tasks = Todo.query.all()
        return render_template('index.html', tasks=tasks, complete_task = complete_task, user=current_user)

        
# Add task with user route
@views.route('/add', methods=['POST'])
@login_required
def add_task():
        user_id = current_user.id
        task = request.form.get('content')
        due_date_iso = request.form.get('dueDate')
        if due_date_iso == '':
            due_date_iso = dt.datetime.now().isoformat(' ')
        due_date = dt.datetime.fromisoformat(due_date_iso)

        new_task = Todo(task=task, due_date=due_date, user_id=user_id)
        if task == "":
            flash('Please enter a task', category='error')
            redirect('/')
        else:
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('views.all_todos'))


# Update task with user route 
@views.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_task(id):
    update_id = Todo.query.get_or_404(id)
    if request.method == 'POST':
        update_id.task = request.form['content']
        if update_id.user_id == current_user.id:
            db.session.commit()
            return redirect(url_for('views.all_todos'))
          
    else:
        return render_template('update.html', update_id=update_id, user=current_user)


# Delete task route
@views.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task_delete = Todo.query.get_or_404(id)
    if task_delete:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect(url_for('views.all_todos'))


# Completed task route
@views.route('/complete/<int:id>', methods=['GET'])
@login_required
def completed_task(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = True
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('views.all_todos'))