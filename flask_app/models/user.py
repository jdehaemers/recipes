from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(self, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL('recipes_schema').query_db(query, data)
    
    @classmethod
    def get_user(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results
    
    @classmethod
    def get_user_recipes(cls, data):
        query = 'SELECT * FROM recipes JOIN users_recipes ON recipes.id = users_recipes.recipe_id WHERE user_id = %(id)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results
        
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('recipes_schema').query_db(query)
        return results
    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL('recipes_schema').query_db(query, data)
    
    @staticmethod
    def validate_registration( user ):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        users = User.get_all()
        for u in users:
            if u['email'] == user['email']:
                flash('Email address already registered')
                is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords must match')
            is_valid = False
        return is_valid