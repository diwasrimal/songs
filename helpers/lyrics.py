from lyrics_extractor import SongLyrics
import music_tag
import os
import re

# Authentication used for lyrics extraction
GCS_API_KEY = os.environ.get("GCS_API_KEY")
GCS_ENGINE_ID = os.environ.get("GCS_ENGINE_ID")

def get_lyrics(name):
	"""Takes a song title, gives back its lyrics"""

	print("📚 Getting lyrics....")

	extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)
	lyrics = extract_lyrics.get_lyrics(name)['lyrics']

	lyrics = ''.join(re.split("\[.*?\]", lyrics))

	print("Returning lyrics")
	return lyrics


def embed_lyrics(song, lyrics):
	"""Embeds lyrics to song's metadata"""
	data = music_tag.load_file(song)
	data['lyrics'] = lyrics
	data.save()


def look_lyrics(song):
	""" Looks embedded lyrics inside a song """
	data = music_tag.load_file(song)
	return str(data['lyrics'])


