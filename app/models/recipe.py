from app.config.mysqlconnection import connectToMySQL
from app.models import user
from flask import flash
class Recipes:
    def __init__(self,data):
        self.id = data['id']
        self.name= data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.poster = None

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.user_id'
        recipe_db = connectToMySQL('recipes').query_db(query)
        recipes = []
        for recipe in recipe_db:
            users = cls(recipe)
            user_data = {
                'id' : recipe['users.id'],
                'first_name' : recipe['first_name'],
                'last_name' : recipe['last_name'],
                'email' : recipe['email'],
                'password' : "",
                'created_at' : recipe['users.created_at'],
                'updated_at' : recipe['users.updated_at']
            }
            users.poster = user.Users(user_data)
            recipes.append(users)
        return recipes
    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s'
        recipes = connectToMySQL('recipes').query_db(query,data)
        
        return cls(recipes[0]) if recipes else None

    @classmethod 
    def delete(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        return connectToMySQL('recipes').query_db(query,data)

    """@classmethod 
    def get_year(cls,data):
        query = 'SELECT YEAR(date_made) FROM recipes WHERE id = %(id)s'
        recipes = connectToMySQL('recipes').query_db(query,data)
        return cls(recipes[0]) if recipes else None"""
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes(name,description,instructions,date_made,under_30,user_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s)"
        return connectToMySQL('recipes').query_db(query,data)
    @classmethod 
    def get_with_user(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE users.id = %(id)s"
        user_row = connectToMySQL('recipes').query_db(query,data)
        users = cls(user_row[0])
        for user_cls in user_row:
            user_data = {
                'id' : user_cls['users.id'],
                'first_name' : user_cls['first_name'],
                'last_name' : user_cls['last_name'],
                'email' : user_cls['email'],
                'password' : "",
                'created_at' : user_cls['users.created_at'],
                'updated_at' : user_cls['users.updated_at']
            }
            users.poster = user.Users(user_data)
        return users
    
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description = %(description)s, instructions =%(instructions)s, date_made=%(date_made)s, under_30 =%(under_30)s WHERE id = %(id)s"
        return connectToMySQL("recipes").query_db(query,data)
    
    @staticmethod
    def recipe_validation(recipe):
        is_valid = True
        if len(recipe['instructions']) < 3:
            flash("instruction must at least be 3 characters")
            is_valid = False
        
        if len(recipe['description']) <3:
            flash("description must at least be 3 characters")
            is_valid = False
        
        if len(recipe['name']) <3:
            flash("name must at least be 3 characters")
            is_valid = False
        if len(recipe['date_made']) == 0:
            flash("date must not be blank")
            is_valid = False
        return is_valid