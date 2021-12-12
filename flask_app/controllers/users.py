from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/')
def index():
    login_errors = {'Incorrect password', 'email not registered'}
    return render_template('index.html', login_errors=login_errors)

@app.route('/register', methods=['POST'])
def submit():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
        }
    User.create(data)
    return redirect('/')

@app.route('/login/user', methods=['POST'])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
        }
    if len(User.get_user(data)) < 1:
        flash('email not registered')
        return redirect('/')
    user = User.get_user(data)[0]
    if not bcrypt.check_password_hash(user['password'], data['password']):
        flash('Incorrect password')
        return redirect('/')
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session['user_first'] = user['first_name']
    session['user_last'] = user['last_name']
    session['logged_in'] = True
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/')
    data = { 'id' : session['user_id']}
    recipes = Recipe.get_all()
    return render_template('dashboard.html', recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
