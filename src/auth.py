from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)



"""
Authorization Flask Login

"""


# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Log in successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.all_todos'))
            else:
                flash('Incorrect password, please try again!', category='error')
        else:
            flash('Email does not exists.', category='error') 


    return render_template('login.html', user=current_user)


# Signup route
@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email') 
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2') 
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.', category='error')    
        elif password1 != password2:
            flash('Passwords do not match, please try again', category='error')
            return redirect(url_for('auth.signup'))
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()           
            flash('Success! Account created. Please login.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html', user=current_user)


# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
