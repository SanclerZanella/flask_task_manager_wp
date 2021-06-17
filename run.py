import os
from flask import (
    Flask, flash,
    render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists('env.py'):
    import env

# Instance of Flask
app = Flask(__name__)

# Grab the database name
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")

# Configure the actual DB connection string
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Secret key required to connect to flash() and session()
# flask functions
app.secret_key = os.environ.get("SECRET_KEY")

# Create an instance of PyMongo
mongo = PyMongo(app)


# Function to execute the registration page and form
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if the username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session['user'] = request.form.get("username").lower()
        flash("Registration Successful")

    return render_template("register.html")


# Function to execute the login page and form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if the username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
            else:
                # Invalid password
                flash("Incorrect username and/or password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Route decorator for the main route and function to execute the main route
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


# Define host and port for the app
# Tell the app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
