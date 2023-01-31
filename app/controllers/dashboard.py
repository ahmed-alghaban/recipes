from app import app,validation
from app.models.recipe import Recipes
from flask import redirect,render_template,session,request,flash

@app.route("/dashboard")
def dashboard():
    if not 'user_id' in session :
        return redirect("/")
    data = {
        "id" : session['user_id']
    }
        
    return render_template("dashboard.html",users = Recipes.get_one(data), recipes = Recipes.get_all())

@app.route("/view/<int:id>")
def view(id):
    data = {
        "id" : id
    }
    user_id = {"id" : session["user_id"]}
    if not 'user_id' in session :
        return redirect("/") 
    return render_template("show_recipes.html",recipes = Recipes.get_one(data),users = Recipes.get_with_user(user_id))

@app.route("/delete/<int:id>")
def delete(id):
    if not 'user_id' in session :
        return redirect("/")
    data = {
        "id" : id
    }
    Recipes.delete(data)
    return redirect("/dashboard")

@app.route("/create")
def create():
    if not 'user_id' in session :
        return redirect("/")
    return render_template("add_recipes.html")

@app.route("/create/recipe", methods = ['POST'])
def create_recipe():
    if not 'user_id' in session :
        return redirect("/")
    under_30 = request.form.get("under_30")
    request_list = ["name","description","instructions","date_made"]
    """for form_data in request_list:
        data = {
            form_data : request.form[form_data],
            "under_30" : 1 if under_30 == "yes" else 0, 
            "user_id" : session["user_id"],
        }"""
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_made" : request.form["date_made"],
        "under_30" : 1 if under_30 == "yes" else 0, 
        "user_id" : session["user_id"],
    }
    recipe = Recipes.save(data)

    if not Recipes.recipe_validation(data):
        return redirect("/create")
    
    return redirect("/dashboard")

@app.route("/update/<int:id>")
def render_update(id):
    if not 'user_id' in session :
        return redirect("/")
    data = {
        "id" :id
    }
    return render_template("edit_recipes.html",recipes = Recipes.get_one(data))

@app.route("/update/<int:id>/recipe",methods =['POST'])
def update(id):
    under_30 = request.form.get("under_30")
    if not 'user_id' in session :
        return redirect("/")
    data = {
    "id" : id,
    "name" : request.form["name"],
    "description" : request.form["description"],
    "instructions" : request.form["instructions"],
    "date_made" : request.form["date_made"],
    "under_30" : 1 if under_30 == "yes" else 0, 
    }
    if not Recipes.recipe_validation(data):
        return redirect(f"/update/{id}")
    Recipes.update(data)
    return redirect("/dashboard")