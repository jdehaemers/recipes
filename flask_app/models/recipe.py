from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['name']
        self.last_name = data['description']
        self.email = data['instructions']
        self.password_hash = data['under_thirty']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, date_made, under_thirty, creator_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s, %(creator_id)s );'
        return connectToMySQL('recipes_schema').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL('recipes_schema').query_db(query)
        return results
    
    @classmethod
    def get_recipe(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(recipe_id)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results
    
    @classmethod
    def assign_recipe(cls, data):
        query = 'INSERT INTO users_recipes (user_id, recipe_id) VALUES ( %(user_id)s, %(recipe_id)s );'
        return connectToMySQL('recipes_schema').query_db(query, data)
        
    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_thirty =%(under_thirty)s WHERE id = %(id)s;'
        return connectToMySQL('recipes_schema').query_db(query, data)
        
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users_recipes WHERE recipe_id = %(id)s;'
        connectToMySQL('recipes_schema').query_db(query, data)
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        connectToMySQL('recipes_schema').query_db(query, data)
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            flash('Must provide recipe name')
            is_valid = False
        if len(recipe['description']) < 1:
            flash('Must provide description')
            is_valid = False
        if len(recipe['instructions']) < 1:
            flash('Must provide instructions')
            is_valid = False
        # if len(recipe['instructions']) < 1:
        #     flash('Must provide instructions')
        #     is_valid = False
        if recipe['date_made'] == '':
            flash('Must provide date')
            is_valid = False
        return is_valid