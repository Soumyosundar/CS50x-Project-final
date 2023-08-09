import os

import math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
            rows = db.execute("SELECT * FROM User_share WHERE user_id = ? ", session["user_id"])
            if len(rows) != 0:
                return render_template("index.html", IndexT=rows)
            else:
                return render_template("index.html")

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add Cash"""

    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("Addcash.html", user_cash=usd(user_cash))

    added_cash = request.form.get("added_cash")
    new_total_cash = float(added_cash) + float(user_cash)
    db.execute("UPDATE users SET cash = ? WHERE id = ?", new_total_cash, session["user_id"])

    return render_template("index.html")



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not (symbol := request.form.get("symbol")):
            return apology("MISSING SYMBOL")

        if not (shares := request.form.get("shares")):
            return apology("NOT ENOUGH SHARES")

        try:
            shares = int(shares)
        except ValueError:
            return apology("INVALID SHARES")

        if not (shares > 0):
            return apology("INVALID SHARES")

        if not (query := lookup(symbol)):
            return apology("CAN'T FIND SYMBOL")

        rows = db.execute("SELECT * FROM users WHERE id = ?;",
                          session["user_id"])

        user_owned_cash = rows[0]["cash"]
        total_prices = query["price"] * shares

        if user_owned_cash < total_prices:
            return apology("NOT ENOUGH MONEY")

        db.execute("INSERT INTO transactions(user_id, symbol, shares, price, Type) VALUES(?, ?, ?, ?, ?);",
                   session["user_id"], symbol, shares, query["price"], "BUY")

        # Update user owned cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                   (user_owned_cash - total_prices), session["user_id"])

        rows = db.execute("SELECT * FROM User_share WHERE user_id = ? and symbol=?;",
                          session["user_id"], request.form.get("symbol"))
        if len(rows) == 0:
            # User does not have the symbol in user share table
            db.execute("INSERT INTO User_share (user_id, symbol, shares, Company Name) VALUES(?, ?, ?);",
                       session["user_id"], symbol, shares, query.companyName)
        else:
            # User Has the syymbol in user share table
            db.execute("UPDATE User_share SET shares = ? WHERE user_id = ? and symbol = ?;",
                       (rows[0]["shares"]+shares), session["user_id"], request.form.get("symbol"))
        flash("Purchased!")

        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ", session["user_id"])
    if len(rows) != 0:
        return render_template("history.html", IndexT=rows)
    else:
        return apology("NO RECORD")

@app.route("/portfolio_analysis")
@login_required
def portfolio_analysis():
    if request.method == "GET":
            rows = db.execute("SELECT symbol, company, sum(shares) as shr, sum(shares*price) as pri FROM transactions WHERE user_id = ? and Type = 'BUY' GROUP BY symbol ", session["user_id"])
            cnt = 0;
            # w, h = 8, 5
            Matrix = [[0 for x in range(5)] for y in range(len(rows))]
            print (len(rows))
            rows1 = db.execute("delete FROM tempTBL")
            while (cnt < len(rows)):
                Matrix[cnt][0]= rows[cnt]["symbol"]
                Matrix[cnt][1]= rows[cnt]["company"]
                Matrix[cnt][2]= rows[cnt]["shr"]
                Matrix[cnt][3]= rows[cnt]["pri"]


                if not (query := lookup(rows[cnt]["symbol"])):
                    return apology("CAN'T FIND SYMBOL")
                else:
                    Matrix[cnt][4]= query["price"]
                    print (Matrix[cnt][0],Matrix[cnt][1],Matrix[cnt][2],Matrix[cnt][3],Matrix[cnt][4],"--------")
            # Creates a list containing 5 lists, each of 8 items, all set to 0

                    db.execute("INSERT INTO tempTBL(F1, F2, F3, F4, F5) VALUES(?, ?, ?, ?, ?);",
                    Matrix[cnt][0], Matrix[cnt][1], Matrix[cnt][2], Matrix[cnt][3], Matrix[cnt][4]*Matrix[cnt][2])
                    cnt=cnt+1
            else:
                if len(rows) != 0:
                    print (Matrix)
                    rows1 = db.execute("SELECT * FROM tempTBL")
                    return render_template("portfolio_analysis.html", IndexT=rows1)
                else:
                    return render_template("portfolio_analysis.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash("logged in!")
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
        if not (query := lookup(request.form.get("symbol"))):
            return apology("INCORRECT SYMBOL")

        return render_template("quote.html", query=query)
    else:
        return render_template("quote.html")

@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    """Allow user to change their password"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("changepassword.html")

    # User reached route via POST (as by submitting a form via POST)
    current_pw = request.form.get("current_password")
    new_pw = request.form.get("new_password")
    confirm_new_pw = request.form.get("confirm_new_password")

    # Check whether the input box for current password is empty or not
    if not current_pw:
        return apology("You should input your current password")

    # Check whether the current password is correct or not
    old_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
    if len(old_password) != 1 or not check_password_hash(old_password[0]["hash"], current_pw):
        return apology("invalid username and/or password", 403)

    # New password and Confirm New Password Validation
    if not new_pw:
        return apology("You should input your new password")
    elif not confirm_new_pw:
        return apology("You should input your password in 'Confirmation New Password'")
    elif new_pw != confirm_new_pw:
        return apology("Password does not match")

    # Update the the new password for that user in database
    hashed_new_pw = generate_password_hash(new_pw)
    db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new_pw, session["user_id"])
    flash("Password Changed")
    # Redirect the user to login form
    return redirect("/logout")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()


    if request.method == "POST":

        if not (username := request.form.get("username")):
            return apology("USERNAME REQUIRED")

        if not (password := request.form.get("password")):
            return apology("PASSWORD REQUIRED")

        if not (confirmation := request.form.get("confirmation")):
            return apology("PASSWORDS DO NOT MATCH THE ORIGINAL")

        # Ensure first password and second password are matched
        if password != confirmation:
            return apology("Password mismatched")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # Ensure username not in database
        if len(rows) == 1:
            return apology("Username '{username}' already exists.")

        else:
            # Insert username into database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                            username, generate_password_hash(password))
# id =
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Remember which user has logged in
            # session["user_id"] = id

            flash("Successfully registered.", "message")

            return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not (symbol := request.form.get("symbol")):
            return apology("MISSING SYMBOL")

        if not (shares := request.form.get("shares")):
            return apology("NOT ENOUGH SHARES")

        try:
            shares = int(shares)
        except ValueError:
            return apology("INVALID SHARES")

        if not (shares > 0):
            return apology("INVALID SHARES")

        if not (query := lookup(symbol)):
            return apology("CAN'T FIND SYMBOL")

        rows = db.execute("SELECT * FROM User_share WHERE user_id = ? and symbol=?;",
                          session["user_id"], request.form.get("symbol"))
        if len(rows) == 0:
            # User does not have the syymbol in user share table
            return apology("YOU DO NOT HAVE THIS SHARE")
        else:
            # User Has the syymbol in user share table
            db.execute("UPDATE User_share SET shares = ? WHERE user_id = ? and symbol = ?;",
                       (rows[0]["shares"]-shares), session["user_id"], request.form.get("symbol"))

        rows = db.execute("SELECT * FROM users WHERE id = ?;",
                          session["user_id"])
        user_owned_cash = rows[0]["cash"]
        total_prices = query["price"] * shares

        # Update user owned cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                   (user_owned_cash + total_prices), session["user_id"])

        db.execute("INSERT INTO transactions(user_id, company, symbol, shares, price, Type) VALUES(?, ?, ?, ?, ?, ?);",
                   session["user_id"], query["name"], symbol, shares, query["price"], "SELL")

        flash("Sold!")

        return redirect("/")
    else:
        return render_template("sell.html")
