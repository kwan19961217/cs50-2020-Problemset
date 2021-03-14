import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pandas as pd
import numpy as np
import re
from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT * FROM own WHERE owner_id = :user_id", user_id = session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"] )
    assets = 0
    for row in rows:
        price = lookup(row['symbol'])['price']
        #add new fields into rows
        row['price'] = price
        row['value'] = price * row['number']
        assets += row['value']
    cash = cash[0]["cash"]
    assets += cash
    return render_template("index.html", rows = rows, cash = cash, assets = assets)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = (request.form.get("symbol")).upper()
        quotes = lookup(symbol)
        #check if the stock exists
        if quotes == None:
            return apology("Stock Not Found")
        #check if the stock number is positive
        if int(request.form.get("number")) <= 0:
            return apology("Invalid Number of Stock")
        price = float(quotes["price"])
        number = int(request.form.get("number"))
        total_cost = price * number
        row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        cash = row[0]["cash"]
        if total_cost < cash:
            cash = cash - total_cost
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            #deduct cash
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash = cash, user_id = session["user_id"])

            #add new buy record
            db.execute("INSERT INTO buy (buyer_id, symbol, number, price, action_time) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], symbol, number, price, dt_string)

            #check if the user already own the same stock
            rows = db.execute("SELECT * FROM own WHERE owner_id = :id AND symbol = :symbol", id = session["user_id"], symbol = symbol)
            if not rows:
                db.execute("INSERT INTO own (owner_id, symbol, number) VALUES (?, ?, ?)",
                           session["user_id"], symbol, number)
                return redirect("/history")
            else:
                db.execute("UPDATE own SET number = number + :number WHERE owner_id = :id AND symbol = :symbol",
                           number = number, id = session["user_id"], symbol = symbol)
                return redirect("/history")
        else:
            return apology("Not Enough Money")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM buy WHERE buyer_id = :id", id = session["user_id"])

    for row in rows:
        row['action'] = ("Buy")

    srows = db.execute("SELECT * FROM sell WHERE seller_id = :id", id = session["user_id"])

    for row in srows:
        row['action']=("Sell")

        #combine the sell history with buy history
        rows.append(row)

    return render_template("history.html", rows = sorted(rows, key = lambda i:i['action_time']))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quotes = {}
        quotes = lookup(request.form.get("symbol"))
        return render_template("quoted.html", quotes = quotes)
    else:
        return render_template("quotes.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 403)

        elif not password:
            return apology("must provide password", 403)

        elif password != request.form.get("confirmation"):
            return apology("Please enter the same password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        if len(rows) != 0:
            return apology("The username already exists!", 403)

        #check the number of character of the password
        elif len(password) < 8:
            return apology("The password must be at least 8 characters")

        #check if the password contains both digits and letters
        elif not re.search(r"[\d]+", password) or not re.search(r"[a-z]+", password):
            return apology("Password must contain at least one digit and letter")

        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                       username = username,
                       hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
            return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = (request.form.get("symbol")).upper()
        quotes = lookup(symbol)
        number = int(request.form.get("number"))

        #check if the stock exists
        if quotes == None:
            return apology("Stock Not Found")

        #check if the number of stocks is positive
        if number <= 0:
            return apology("Invalid Number of Stock")

        #check if the user actually owns the stock
        row = db.execute("SELECT * FROM own WHERE owner_id = :id AND symbol = :symbol", id = session["user_id"], symbol = symbol)
        if not row:
            return apology("Not Enough Shares")

        #check if the user has enough stock
        elif number > row[0]["number"]:
            return apology("Not Enough Shares")

        else:
            price = float(quotes["price"])
            revenue = price * number
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            #change number of owned stock
            db.execute("UPDATE own SET number = number - :number WHERE owner_id = :id AND symbol = :symbol",
                       number = number, id = session["user_id"], symbol = symbol)
            #add cash
            db.execute("UPDATE users SET cash = cash + :revenue WHERE id = :user_id", revenue = revenue, user_id = session["user_id"])

            #add sell record
            db.execute("INSERT INTO sell (seller_id, symbol, number, price, action_time) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], symbol, number, price, dt_string)

        #delete the record from own if no more own the stock
        row = db.execute("SELECT number FROM own WHERE owner_id = :id AND symbol = :symbol", id = session["user_id"], symbol = symbol)
        if row[0]["number"] == 0:
            db.execute("DELETE FROM own WHERE owner_id = :id AND symbol = :symbol", id = session["user_id"], symbol = symbol)
        return redirect("/history")
    return render_template("sell.html")

@app.route("/change_pw", methods=["GET", "POST"])
@login_required
def change_pw():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        newpw = request.form.get("newpw")

        # Ensure username was submitted
        if not request.form.get("oldpw"):
            return apology("must provide old password", 403)

        # Ensure password was submitted
        elif not request.form.get("newpw"):
            return apology("must provide new password", 403)
        elif not request.form.get("newpw2"):
            return apology("must confirm new password", 403)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session["user_id"])

        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("oldpw")):
            return apology("invalid old password", 403)
        elif request.form.get("newpw") != request.form.get("newpw2"):
            return apology("Cannot confirm password")

        #check the number of character of the password
        elif len(newpw) < 8:
            return apology("The password must be at least 8 characters")

        #check if the password contains both digits and letters
        elif not re.search(r"[\d]+", newpw) or not re.search(r"[a-z]+", newpw):
            return apology("Password must contain at least one digit and letter")

        else:
            db.execute("UPDATE users SET hash = :hash WHERE id = :id",
                       id=session["user_id"], hash=generate_password_hash(newpw, method='pbkdf2:sha256', salt_length=8))
            return redirect("/")
    return render_template("change_pw.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
