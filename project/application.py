import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import re

from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pawmark.db")

#login_required function credited to cs50
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if password != request.form.get("confirmation"):
            flash("Please input the same password!")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        #check if the user exists
        if len(rows) != 0:
            flash("The username already exists!")
            return render_template("register.html")

        #check the number of character of the password
        elif len(password) < 8:
            flash("The password must be at least 8 characters!")
            return render_template("register.html")

        #check if the password contains both digits and letters
        elif not re.search(r"[\d]+", password) or not re.search(r"[a-z]+", password):
            flash("Password must contain at least one digit and letter!")
            return render_template("register.html")

        #successfully registered
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                       username = username,
                       hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
            #login
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=username)
            session["user_id"] = rows[0]["id"]
            return render_template("update.html")
    else:
        return render_template("register.html")

#login and logout function credited to cs50
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username or password!")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        name = request.form.get("name").title()
        photo = request.form.get("photo")
        mb_region = request.form.get("mb_region")
        mb_no = request.form.get("mb_no")
        email = request.form.get("email")
        db.execute("UPDATE users SET name = :name, photo = :photo, mb_region = :mb_region, mb_no = :mb_no, email = :email WHERE id = :id",
                   id = session["user_id"], name = name, photo = photo, mb_region = mb_region, mb_no = mb_no, email = email)
        return redirect("/")
    row = db.execute("SELECT * FROM users WHERE id = :id", id =session["user_id"])
    return render_template("update.html", row = row)

@app.route("/add_pet", methods=["GET", "POST"])
@login_required
def add_pet():
    if request.method == "POST":
        pet_name = request.form.get("pet_name").title()
        rows = db.execute("SELECT * FROM pets WHERE owner_id = :owner_id AND pet_name = :pet_name", owner_id = session["user_id"], pet_name = pet_name)
        if len(rows) != 0:
            flash("Duplicate Pet Name!")
            return redirect("/")
        gender = request.form.get("gender").title()
        species = request.form.get("species").title()
        breeds = request.form.get("breeds").title()
        pet_photo = request.form.get("pet_photo")
        color = request.form.get("color").title()
        pattern = request.form.get("pattern").title()
        city = request.form.get("city").title()
        district = request.form.get("district").title()
        age =request.form.get("age")
        db.execute("INSERT INTO pets (owner_id, pet_name, gender, species, breeds, pet_photo, color, pattern, city, district, age) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], pet_name, gender, species, breeds, pet_photo, color, pattern, city, district, age)
        return redirect("/")
    return render_template("add_pet.html")

@app.route("/select_update_pet", methods=["GET", "POST"])
@login_required
def select_update_pet():
    if request.method == "POST":
        pet_name = request.form.get("pet_name").title()
        rows = db.execute("SELECT * FROM pets WHERE owner_id = :owner_id AND pet_name = :pet_name", owner_id = session["user_id"], pet_name = pet_name)
        if not rows:
            flash("Pet Not Found")
            return redirect("/")
        else:
            return render_template("update_pet.html", rows = rows)
    rows = db.execute("SELECT * FROM pets WHERE owner_id = :owner_id", owner_id = session["user_id"])
    return render_template("select_update_pet.html", rows = rows)

@app.route("/update_pet", methods=["GET", "POST"])
@login_required
def update_pet():
    if request.method == "POST":
        pet_name = request.form.get("pet_name").title()
        rows = db.execute("SELECT * FROM pets WHERE owner_id = :owner_id AND pet_name = :pet_name", owner_id = session["user_id"], pet_name = pet_name)
        gender = request.form.get("gender").title()
        species = request.form.get("species").title()
        breeds = request.form.get("breeds").title()
        pet_photo = request.form.get("pet_photo")
        color = request.form.get("color").title()
        pattern = request.form.get("pattern").title()
        city = request.form.get("city").title()
        district = request.form.get("district").title()
        age =request.form.get("age")
        db.execute("UPDATE pets SET gender = :gender, species = :species, breeds = :breeds, pet_photo = :pet_photo, color = :color, pattern = :pattern, city = :city, district = :district, age = :age WHERE owner_id = :owner_id AND pet_name = :pet_name",
                    owner_id = session["user_id"], pet_name = pet_name, gender = gender, species = species, breeds = breeds, pet_photo = pet_photo, color = color, pattern = pattern, city = city, district = district, age = age)
        return redirect("/")



@app.route("/search_pet", methods=["GET"])
@login_required
def search_pet():
    key = request.args.get("key")
    rows = db.execute("SELECT * FROM pets JOIN users ON pets.owner_id = users.id WHERE pet_name LIKE ? OR gender LIKE ? OR species LIKE ? OR breeds LIKE ? OR color LIKE ? OR pattern LIKE ? OR city LIKE ? OR district LIKE ?", ("%" + key + "%"), (key), ("%" + key + "%"), ("%" + key + "%"), ("%" + key + "%"), ("%" + key + "%"), ("%" + key + "%"), ("%" + key + "%"))
    return render_template("select_pet.html", rows = rows)



@app.route("/search_user", methods=["GET"])
@login_required
def search_user():
    key = request.args.get("key")
    rows = db.execute("SELECT * FROM users WHERE name LIKE ? OR email LIKE ?", ("%" + key + "%"), ("%" + key + "%"))
    pet_rows = db.execute("SELECT * FROM users JOIN pets ON users.id = pets.owner_id WHERE name LIKE ? OR email LIKE ?", ("%" + key + "%"), ("%" + key + "%"))
    return render_template("select_user.html", rows = rows, pet_rows = pet_rows)

@app.route("/link_pet", methods=["GET"])
@login_required
def link_pet():
    #owner_id = request.args.get("owner_id")
    #pet_name = request.args.get("pet_name")
    #rows = db.execute("SELECT * FROM pets JOIN users ON pets.owner_id = users.id WHERE pet_name = :pet_name AND owner_id = :owner_id", pet_name = pet_name, owner_id = owner_id)
    pet_id = request.args.get("pet_id")
    rows = db.execute("SELECT * FROM pets JOIN users ON pets.owner_id = users.id WHERE pet_id = :pet_id", pet_id = pet_id)
    return render_template("select_pet.html", rows = rows)



@app.route("/delete_pet", methods=["GET", "POST"])
@login_required
def delete_pet():
    if request.method == "POST":
        pet_name = request.form.get("pet_name").title()
        db.execute("DELETE FROM pets WHERE pet_name = :pet_name AND owner_id = :owner_id", pet_name = pet_name, owner_id = session["user_id"])
        return redirect("/")
    rows = db.execute("SELECT * FROM pets WHERE owner_id = :owner_id", owner_id = session["user_id"])
    return render_template("delete_pet.html", rows = rows)

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    rows = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
    prows = db.execute("SELECT * FROM pets WHERE owner_id = :id", id = session["user_id"])
    return render_template("profile.html",rows = rows, prows = prows)