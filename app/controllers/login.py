from app import app
from app.models.user import Users
from flask import redirect,render_template,session,request,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/register", methods = ['POST'])
def register_user():
    password = ""
    if len(request.form['password']) > 0 :
        password = bcrypt.generate_password_hash(request.form['password']) 
    data = {
        "fname" : request.form['fname'],
        "lname" : request.form['lname'],
        "email" : request.form['email'],
        "password" : password
        }
    if not Users.user_validation(data):
        return redirect("/")    
    user_id = Users.save(data)
    session['user_id'] = user_id
    return redirect(f"/dashboard")

@app.route("/login", methods = ['POST'])
def login():
    
    user = Users.get_by_email(request.form['email_address'])
    if not user or not bcrypt.check_password_hash(user.password,request.form['password_login']):
        flash('Invalid credentials','login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect(f'/dashboard')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")