from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes

@app.route("/")
@app.route("/sign-up")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home")
@app.route("/surf-central")
def home():
    return render_template("home.html")

@app.route("/find-a-duo")
def findaduo():
    return render_template("findaduo.html")

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
