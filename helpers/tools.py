from flask import redirect, render_template, session
from functools import wraps
from platform import system
from time import time


"""Render message as an apology to user."""
def apology(message, code=400):
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def corrected_path(path):
    """Autocorrects filepaths"""
    if system() == "Windows": 
        return path.replace('/', '\\') 
    return path

def time_taken(f):
    @wraps(f)
    def inner(*args, **kwargs):
        start = time()
        ret = f(*args, **kwargs)
        print(f"⏰ Time elapsed: {time() - start}\n")
        return ret
    return inner



