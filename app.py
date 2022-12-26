from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from threading import Thread
from cs50 import SQL
import os

from helpers.tools  import apology, login_required, corrected_path, time_taken
from helpers.songs  import search_song, download_song
from helpers.lyrics import get_lyrics, embed_lyrics, look_lyrics

# Configure Flask application
app = Flask(__name__)

# Ensure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///music.db")

# Downloaded songs go here (corrected_path returns platform specific path)
STORAGE = corrected_path('static/downloads/audio')

# Make sure GCS_ENGINE_ID is set
if not os.environ.get("GCS_ENGINE_ID"):
    raise RuntimeError("GCS_ENGINE_ID not set")

# Make sure GCS_API_KEY  is set
if not os.environ.get("GCS_API_KEY"):
    raise RuntimeError("GCS_API_KEY not set")


##
### Routes
##

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
        flash("Registered!", "success")
        return redirect("/")


@app.route("/search")
@login_required
def search():

    # Delete previous searches
    db.execute("DELETE FROM searches")

    name = request.args.get("name")
    songs = search_song(name)

    # Flash error message if song not found!
    if songs == []:
        flash("No matching results!", "danger")
        return redirect("/")

    # Temporarily store searches (will be used in /play)
    for song in songs:
        db.execute("INSERT INTO searches(id, title, channel, thumbnail) VALUES (?, ?, ?, ?)", 
            song['id'], song['title'], song['channel'], song['thumbnail'])

    return render_template("searchResults.html", songs=songs)


@app.route("/play")
@login_required
@time_taken
def play():

    # Get info in that song
    id = request.args.get('songId')
    if not id or id == '':
        return render_template("play.html")

    # Check if song is in database
    result = db.execute("SELECT * FROM songs WHERE id = ?", id)

    # Song is in database. Retrieve data from there
    if result != []:
        song = result[0]
        lyrics = look_lyrics(song['path'])

    # Song was not in database, make a new record 
    else:

        # Check if user played new song
        searched = db.execute("SELECT * FROM searches WHERE id = ?", id)
        if searched == []:          # Song was neither in database nor was searched by user
            return apology("Song not found!")

        # Get basic details from searches
        song = searched[0]

        # Use threading for concurrent lyrics fetching and download.
        # Create a List to store the lyrics while the thread runs.
        # And access the list after the song gets downloaded.
        # That way we'll have more than enough time to get lyrics
        lyrics_list = []
        def get_lyrics_thread_target():
            try:
                lyrics = get_lyrics(song['title']).replace('\n\n', '\n')
            except Exception:
                lyrics = "Could not find lyrics"
            lyrics_list.append(lyrics)
        
        # Start the thread
        Thread(target=get_lyrics_thread_target).start()

        # Download song in a unique id denoted folder 
        song_folder = corrected_path(f"{STORAGE}/{id}")
        if song_folder not in os.listdir(STORAGE):
            os.system(f"mkdir {song_folder}")
            download_song(song_folder, id)

        # Set song's path
        song['path'] = corrected_path(f"{song_folder}/{os.listdir(song_folder)[0]}")

        # Record
        db.execute(
            "INSERT INTO songs(id, title, channel, thumbnail, path) VALUES (?, ?, ?, ?, ?)", 
            song['id'], song['title'], song['channel'], song['thumbnail'], song['path']
            )

        # Embed lyrics inside song's metadata
        lyrics = lyrics_list[0]
        embed_lyrics(song['path'], lyrics)


    # Record song in recently played list
    try:
        if id not in session['recents']:
            session['recents'].append(id)
    except KeyError:
        session['recents'] = [id]

    # Set previous and next song 
    idx = session['recents'].index(id)  # Current song's index in recents list
    song['prevSong'] = session['recents'][idx - 1] if idx > 0 else id
    song['nextSong'] = session['recents'][idx + 1] if idx < (len(session['recents']) - 1) else id

    
    # See if song is favorite or not
    result = db.execute("SELECT * FROM favorites WHERE user_id = ? AND song_id = ?", session['user_id'], id)
    song['favorite'] = True if len(result) != 0 else False

    # Modify lyrics to render as html
    song['lyrics'] = lyrics.replace('\n', '<br>')

    # Details shown in terminal for debugging issues
    # print('\n')
    # for v in song.values():
    #     print(v)
    # print('\n')

    return render_template("play.html", song=song)


# @app.route("/profile")
# @login_required
# def profile():
#     return render_template("profile.html")


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """ Adds/Removes songs from favorites """

    # If requested to add/remove song from favorites
    if request.method == "POST":

        # Get song id from play.html
        song = request.json['songId']
        if not song:
            return apology("An error occured!")

        title = db.execute("SELECT title FROM songs WHERE id = ?", song)[0]['title']

        # Search song in database
        result = db.execute("SELECT * FROM favorites WHERE user_id = ? AND song_id = ?", session['user_id'], song)

        # Add song to favorites if not listed else remove
        if result == []:
            db.execute("INSERT INTO favorites(user_id, song_id) VALUES(?, ?)", session['user_id'], song)
            return f"Added {title}"
        else:
            db.execute("DELETE FROM favorites WHERE user_id = ? AND song_id = ?", session['user_id'], song)
            return f"Removed {title}"

    # If requested via GET
    else:

        # Collect data from database
        results = db.execute("SELECT * FROM favorites WHERE user_id = ?", session['user_id'])
        if results == []:
            return render_template("favorites.html")

        favorites = []
        for res in results:
            song_info = db.execute("SELECT * FROM songs WHERE id = ?", res['song_id'])[0]
            favorites.append(song_info)

        return render_template("favorites.html", favorites=favorites)
