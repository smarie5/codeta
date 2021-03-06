from flask import request, session, g, redirect, url_for, \
        abort, render_template, flash

from flask.ext.login import (current_user, login_required,
        login_user, logout_user, confirm_login,
        fresh_login_required)

from codeta import app, db, login_manager

@app.before_request
def before_request():
    g.user = current_user

# views
@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    """ Register the user for an account """
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You must enter a username.'
        elif not request.form['password']:
            error = 'You must enter a password.'
        elif not request.form['email'] or '@' not in request.form['email']:
            error = 'You must enter a valid email address.'
        elif request.form['password'] != request.form['password2']:
            error = 'Your passwords did not match.'
        elif app.db.get_username(request.form['username']):
            error = 'Sorry, that username is already taken.'
        elif not error:
            db = app.db.get_db()

            sql = "INSERT INTO Users (username, password, email, first_name, last_name) \
                VALUES (%s, %s, %s, %s, %s);"
            data = (
                request.form['username'],
                request.form['password'],
                request.form['email'],
                request.form['fname'],
                request.form['lname'],
            )

            db.cursor().execute(sql, data)
            db.commit()
            flash('You successfully joined, welcome!')
            return redirect(url_for('login'))
    return render_template('join.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login user
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'Invalid username.'
        elif not request.form['password']:
            error = 'Invalid password.'
        else:
            user = app.db.auth_user(
                    request.form['username'],
                    request.form['password'])
            if user:
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                error = 'Invalid username or password.'

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You logged out.'
