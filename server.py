from app import app 
from app.controllers import login,dashboard
if __name__ == ("__main__"):
    app.run(debug=True)