import innertube
import json
import os
import re

from flask import redirect, render_template, request, session
from functools import wraps
from lyrics_extractor import SongLyrics

def search_song(q):
	client = innertube.InnerTube("WEB")
	data = client.search(q)

	# Retrieve list of useful searches
	contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
	data = []

	# Loop through some portion of contents and collect info
	for i in range(len(contents)):
		
		try:
			videoContent = contents[i]['videoRenderer']
		except KeyError:
			break

		thumbnail = videoContent['thumbnail']['thumbnails']
		data.append({
			'id': videoContent['videoId'],
			# 'thumbnail': {
			# 	'url': thumbnail[0]['url'],
			# 	'width': thumbnail[0]['width'],
			# 	'height': thumbnail[0]['height']
			# },
			'thumbnail': thumbnail[0]['url'],
			'title': videoContent['title']['runs'][0]['text'],
			'channel': videoContent['ownerText']['runs'][0]['text']
			})

	return data


def get_lyrics(name):
	
	# Contact engine
	gcs_engine_id = os.environ.get("GCS_API_KEY")
	gcs_api_key = os.environ.get("GCS_ENGINE_ID")

	# Extract data
	extract_lyrics = SongLyrics(gcs_engine_id, gcs_api_key)
	lyrics = extract_lyrics.get_lyrics(name)['lyrics']

	lyrics = ''.join(re.split("\[.*?\]", lyrics))

	return lyrics


def apology(message, code=400):
    """Render message as an apology to user."""
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