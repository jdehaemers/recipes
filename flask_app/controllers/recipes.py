from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.recipe import Recipe

@app.route('/recipe/new')
def new_recipe():
    if 'logged_in' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if 'logged_in' not in session:
        return redirect('/')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty'],
        'creator_id' : session['user_id']
        }
    if not Recipe.validate_recipe(data):
        return redirect('/recipe/new')
    recipe_id = Recipe.create(data)
    assignment_data = {
        'user_id' : session['user_id'],
        'recipe_id' : recipe_id
        }
    Recipe.assign_recipe(assignment_data)
    return redirect('/dashboard')

@app.route('/recipe/<id>')
def view_instructions(id):
    if 'logged_in' not in session:
        return redirect('/')
    data = { 'recipe_id' : id }
    recipe = Recipe.get_recipe(data)[0]
    return render_template('recipes.html', recipe=recipe)

@app.route('/recipe/edit/<id>')
def edit_recipe(id):
    if 'logged_in' not in session:
        return redirect('/')
    data = { 'recipe_id' : id }
    recipe = Recipe.get_recipe(data)[0]
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/update_recipe/<id>', methods=['POST'])
def update_recipe(id):
    if 'logged_in' not in session:
        return redirect('/')
    data = {
        'id' : id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty']
        }
    if not Recipe.validate_recipe(data):
        return redirect(f'/recipe/edit/{id}')
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/recipe/delete/<id>')
def delete_recipe(id):
    if 'logged_in' not in session:
        return redirect('/')
    data = {'id' : id}
    Recipe.delete(data)
    return redirect('/dashboard')