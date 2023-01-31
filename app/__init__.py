from flask import Flask,session,redirect
app = Flask(__name__)

app.secret_key = "ANYthing"

def validation():
    if not 'user_id' in session :
        return redirect("/")