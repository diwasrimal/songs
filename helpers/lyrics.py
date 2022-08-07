import music_tag
import re
import os

from lyrics_extractor import SongLyrics

# Authentication used for lyrics extraction
GCS_ENGINE_ID = os.environ.get("GCS_API_KEY")
GCS_API_KEY = os.environ.get("GCS_ENGINE_ID")

# Retrieves lyrics using lyrics_extractor module
def get_lyrics(name):

	print("Getting lyrics....")

	extract_lyrics = SongLyrics(GCS_ENGINE_ID, GCS_API_KEY)
	lyrics = extract_lyrics.get_lyrics(name)['lyrics']

	lyrics = ''.join(re.split("\[.*?\]", lyrics))

	print("Returning lyrics")
	return lyrics


# Embeds lyrics to song's metadata
def embed_lyrics(song, lyrics):
	data = music_tag.load_file(song)
	data['lyrics'] = lyrics
	data.save()


# Look embedded lyrics inside a song
def look_lyrics(song):
	data = music_tag.load_file(song)
	return str(data['lyrics'])


