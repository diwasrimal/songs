from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
import os

from helpers import apology, login_required, search_song

app = Flask(__name__)

# Ensure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///music.db")

# Dir where donwloaded songs are
STORAGE = 'static/downloads/audio'


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "danger")
            return redirect("/login")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Must provide password", "danger")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username or password", "danger")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

"""Log user out"""
@app.route("/logout")
def logout():

    # Forget any user_id and redirect to login
    session.clear()
    return redirect("/")


"""Register user"""
@app.route("/register", methods=["GET", "POST"])
def register():

    # Just render the HTML page if requested using GET
    if request.method == "GET":
        return render_template("register.html")

    # Register user if requested using POST
    if request.method == "POST":

        # Get user info
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate registration
        # Ensure username was submitted
        if not username:
            flash("Must provide username", "danger")
            return redirect("/register")

        # Ensure that username was unique(not already taken)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:      # Username already registered
            flash("Username not available", "danger")
            return redirect("/register")

        # Ensure password was submitted
        elif not password:
            flash("Must provide password", "danger")
            return redirect("/register")

        elif not confirmation or confirmation != password:
            flash("Passwords do not match", "danger")
            return redirect("/register")

        # Register user
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)

        # Redirect to index page
        return redirect("/")


@app.route("/search")
@login_required
def search():
    return render_template("search.html")


@app.route("/results")
@login_required
def results():
    name = request.args.get("name")
    songs = search_song(name)

    # Record song uniquely in database
    for song in songs:
        try:
            db.execute("INSERT INTO songs(id, title, thumbnail, channel) VALUES (?, ?, ?, ?)", song['id'], song['title'], song['thumbnail'], song['channel'] )
        except ValueError:
            continue

    return render_template("results.html", songs=songs)


@app.route("/play")
@login_required
def play():

    song = request.args.get('songId')

    # Record the song if not in recents 
    if not 'recents' in session: 
        session['recents'] = []
    session['recents'].append(song)

    # Current song's index in recents list
    idx = session['recents'].index(song)

    print()
    print(session['recents'])

    # Get song details and set prev and next song
    details = db.execute("SELECT * FROM songs WHERE id = ?", song)[0]
    details['prevSong'] = session['recents'][idx - 1] if idx > 0 else song
    details['nextSong'] = session['recents'][idx + 1] if idx < (len(session['recents']) - 1) else song
    
    print()
    print(session['recents'])
    print(details['prevSong'])
    print(details['nextSong'])
    print()

    # Download song if not downloaded
    files  = os.listdir(STORAGE)
    if f"{song}.opus" not in files:
        os.system(f'yt-dlp https://www.youtube.com/watch?v={song}')

    return render_template('play.html', details=details)


@app.route("/test")
def test():

    return render_template("test.html")



@app.route("/profile")
@login_required
def profile():
    return apology("OK")


@app.route("/playlist")
@login_required
def playlist():
    return apology("TODO")


@app.route("/top")
@login_required
def top():
    return apology("TODO")
