from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        account = request.form.get('account_type')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password) and (account == user.account_type):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.account_type == 'teacher':
                    return redirect(url_for('views.teacher_page'))
                else:
                    return redirect(url_for('views.student_page'))
            elif check_password_hash(user.password, password) and (account != user.account_type):
                flash('Incorrect account type, try again.', category='error')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return redirect(url_for('views.home'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        account = request.form.get('account_type')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif account == 'Select Account Type':
            flash('Please select an account type.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), account_type=account)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            if new_user.account_type == 'teacher':
                return redirect(url_for('views.teacher_page'))
            else:
                return redirect(url_for('views.student_page'))

    return redirect(url_for('views.home'))
