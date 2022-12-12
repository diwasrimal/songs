import os
import sys
import music_tag
import re

from platform import system
from youtube_title_parse import get_artist_title
from colorama import Fore, Style
from helpers.songs import search_song

CACHE = ".download_cache"

def main():

    usage = ('''Usage:
    python download.py -q song1 song2 youtube-link ... (Quick download)
    python download.py -i                              (Interactive download) 
    ''')
    if len(sys.argv) < 2:
        sys.exit(usage)

    # Songs to download
    song_ids = []
    songs_not_found = []
    songs_queried = 0

    # Quick download
    if sys.argv[1] == '-q':

        # Exit if no songs given
        songs = sys.argv[2:]
        songs_queried = len(songs)
        if not songs:
            warn("No songs specified!")
            sys.exit()

        print("Searching...")
        for song in songs:

            # A youtube link can also be given
            if matches := re.search(r'^https://(?:www\.)?youtu\.?be(?:\.com)?/(?:watch\?v=)?(.*)', song):
                song_ids.append(matches.group(1))
                continue

            result = search_song(song)
            try:
                song_ids.append(result[0]['id'])
            except IndexError:
                print(f"'{song}' not found!")
                songs_not_found.append(song)
                continue

    # Step by Step (Interactive) download
    elif sys.argv[1] == '-i':
        song_ids = collect_songs()
        songs_queried = len(song_ids)
    else:
        sys.exit(usage)

    if not song_ids:
        sys.exit("Nothing to download!")

    # Prompt for a saving path
    path = os.path.expanduser(
            input("Download path (default '$XDG_MUSIC_DIR'  or '~/Music'): ")
            or os.getenv("XDG_MUSIC_DIR") or "~/Music")
    if path.endswith('/'):
        path = path[:-1]

    # Download collected or given songs
    download_songs(song_ids)

    # Make dir to store downloaded songs
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

    # Modify metadata, rename and move the song
    print("Moving files to destination..")
    song_files = os.listdir(CACHE)
    for file in song_files:

        title, ext = ''.join(file.split('.')[:-1]), file.split('.')[-1]

        song_title = ""
        try:
            # Write metadata
            data = music_tag.load_file(f"{CACHE}/{file}")
            artist, song_title = get_artist_title(title)
            data['tracktitle'] = song_title
            data['artist'] = artist
            data.save()
        except Exception as e:
            # print(f"{e} while parsing {file}, skipping...")
            print(f"Error parsing metadata for {file}, skipping..")
            pass

        # Move the file
        new_file = f"{song_title}.{ext}" if song_title else file
        os.rename(f"{CACHE}/{file}", f"{path}/{new_file}")

    # Show songs not found while quick downloading
    failed_songs = len(songs_not_found)
    if failed_songs > 0:
        warn(f"\nFailed downloads")
        for song_not_found in songs_not_found:
            print(song_not_found)

    # Show download status
    print(f"\n{songs_queried} song(s) queried, {songs_queried - failed_songs} downloaded, {failed_songs} failed.")

"""Collect Songs one by one"""
def collect_songs():

    ids = []

    print("Mention songs to downlaod, hit 'd' when done")
    while True:
        query = input(">> ")
        if query == 'd':
            break

        # A youtube link can also be given
        if matches := re.search(r'^https://(?:www\.)?youtu\.?be(?:\.com)?/(?:watch\?v=)?(.*)', query):
            ids.append(matches.group(1))
            print("Added")
            continue

        results = search_song(query)
        if not results:
            print("Song not found, try again")
            continue

        # Confirm song
        title = results[0]['title']
        ans = input(f">> {title} ? (y/n) ")
        if ans == 'n':
            print("Discarded")
            continue
        print("Added")

        # Store song's info in a list
        ids.append(results[0]['id'])

    return ids


"""Download songs using yt-dlp"""
def download_songs(song_ids):

    # Download songs in a cache folder
    print("Starting download...\n")
    if system() == "Linux":
        output_template = f"-o {CACHE}/%\\(title\\)s.%\\(ext\\)s"
    else:
        output_template = f"-o {CACHE}/%(title)s.%(ext)s"
    for id in song_ids:
        os.system(f"yt-dlp {output_template} https://www.youtube.com/watch?v={id}")
        print()


"""Display a warning message"""
def warn(text):
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
