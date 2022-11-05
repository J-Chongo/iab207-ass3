from flask import ( 
    Blueprint, flash, render_template, url_for, redirect, session
) 
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


# create a blueprint
bp = Blueprint('auth', __name__)


# log in page
@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        _username = login_form.username.data
        _password = login_form.password.data
        u1 = User.query.filter_by(username=_username).first()
        if u1 is None:
            error='Incorrect username'
        elif not check_password_hash(u1.password, _password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            session['username'] = _username
            flash("You have successfully logged in")
            return redirect(url_for('main.index'))
        else:
            flash(error)
    # render the page
    return render_template('user.html', form=login_form, heading='Login')

# register page
@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if (register_form.validate_on_submit() == True):
        _username =register_form.username.data
        _password = register_form.password.data
        _email=register_form.email.data
        _phone=register_form.phone.data
        _address=register_form.address.data
        u1 = User.query.filter_by(username=_username).first()

        # if a username already exists in the db
        if u1:
            flash('Username already exists, maybe try logging in instead')
            return redirect(url_for('auth.login'))

        # add user to database with password hash
        password_hash = generate_password_hash(_password)
        new_user = User(username=_username, password=password_hash, 
        email=_email, phone = _phone, address=_address)
        db.session.add(new_user)
        db.session.commit()

        flash("Successfully registered an account")

        # redirect to login page
        return redirect(url_for('auth.login'))
    else:
        # render the page
        return render_template('user.html', form=register_form, heading='Register')

# logout page
@bp.route('/logout')
@login_required
def logout():
    # logs out the user
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']

    flash("Successfully logged out")

    # return user to homepage
    return redirect(url_for('main.index'))
