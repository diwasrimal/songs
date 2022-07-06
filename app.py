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

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/login")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
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

    session.clear()

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
            return apology("must provide username", 400)

        # Ensure that username was unique(not already taken)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:      # Username already registered
            return apology("Username not available")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        elif not confirmation or confirmation != password:
            return apology("passwords do not match", 400)

        # Register user
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)

        # Redirect to stocks page
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

    # Request from results.html 
    song_id = request.args.get('songId')

    if not song_id:
        # Request from play.html to change song
        # If so, we retrieve songId of prev/next requested song from session['recents']
        song_pos = request.args.get('songPos')
        curr_song_id = request.args.get('currSongId')

        if song_pos and curr_song_id:
            curr_song_idx = session['recents'].index(curr_song_id)

            if curr_song_idx >= 0:
                if song_pos == 'previous':
                    song_id = session['recents'][curr_song_idx - 1]
                elif song_pos == 'next':
                    song_id = session['recents'][curr_song_idx + 1]
            else:
                song_id = curr_song_id

    # Record the song in recents
    try:
        if not song_id in session['recents']:
            session['recents'].append(song_id)
    except KeyError:
        session['recents'] = [song_id]

    print("Here's the recnts list")
    print(session['recents'])

    

    song_file = f"{song_id}.opus"

    # Download song if not downloaded
    files  = os.listdir(STORAGE)
    if song_file not in files:
        os.system(f'yt-dlp https://www.youtube.com/watch?v={song_id}')    

    # Get song details
    details = db.execute("SELECT * FROM songs WHERE id = ?", song_id)[0]

    return render_template('play.html', details=details)



@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/profile")
@login_required
def profile():
    return apology("TODO")


@app.route("/playlist")
@login_required
def playlist():
    return apology("TODO")



@app.route("/top")
@login_required
def top():
    return apology("TODO")
