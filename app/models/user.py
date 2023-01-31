from app.config.mysqlconnection import connectToMySQL
import re
from flask import flash,request
from app.models import recipe
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe_class = []
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        user_data = connectToMySQL("recipes").query_db(query)
        user_row = []
        for user in user_data:
            user_row.append(cls(user))
        return user_row
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        user_data_with_id = connectToMySQL("recipes").query_db(query,data)
        return cls(user_data_with_id[0]) if user_data_with_id else None
    
    @classmethod 
    def save(cls,data):
        query = "INSERT INTO users(first_name,last_name,email,password) VALUES(%(fname)s,%(lname)s,%(email)s,%(password)s)"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod 
    def get_by_email(cls,email_address):
        query = "SELECT * FROM users WHERE email = %(email_address)s"
        result = connectToMySQL('recipes').query_db(query,{"email_address" :email_address})
        return cls(result[0]) if result else None

    @staticmethod
    def user_validation(user):
        is_valid = True
        if len(user['fname']) < 2 :
            flash ("First must be at least 2 charecters")
            is_valid = False
        
        if len(user['lname']) <2 :
            flash ("Last must be at least 2 charecters")
            is_valid = False
            
        if len(user['password']) < 8 or len(user['password']) == 0:
            flash("password must be at least 8 charecters")
            is_valid = False
            
        if  request.form['confirm'] != request.form['password']:
            flash("passwords are not matching")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid 