import os
import sys
import music_tag

from platform import system
from youtube_title_parse import get_artist_title
from helpers.songs import search_song

CACHE = ".downlaod_cache"

def main():

    usage = ('''Usage:
    python download.py -i      (Interactive download) 
    python download.py -q      (Quick download)
    ''')
    if len(sys.argv) < 2:
        sys.exit(usage)

    # Songs to download
    song_ids = []

    # Quick download
    if sys.argv[1] == '-q':
        songs = sys.argv[2:]
        for song in songs:
            result = search_song(song)
            try:
                song_ids.append(result[0]['id'])
            except IndexError:
                print(f"{song} not found, try again!")
                continue

    # Step by Step (Inteactive) download
    elif sys.argv[1] == '-i':
        song_ids = collect_songs()
    else:
        sys.exit(usage)

    if not song_ids:
        sys.exit("No songs specified.")

    # Prompt for a saving path
    path = input("Download path (default '~/Music/'): ") or '~/Music'
    if path.endswith('/'):
        path = path[:-1]

    # Download collected or given songs
    download_songs(song_ids)

    # Modify metadata of downloaded songs
    song_files = os.listdir(CACHE)
    for file in song_files:

        # Get artist name and song_title from song_filename
        title, ext = ''.join(file.split('.')[:-1]), file.split('.')[-1]
        artist, song_title = get_artist_title(title)   # Parsing artist and song_title from youtube video title

        # Write metadata information
        data = music_tag.load_file(f"{CACHE}/{file}")
        data['tracktitle'] = song_title
        data['artist'] = artist
        data.save()

        # Rename the file itself
        new_file = f"{song_title}.{ext}"
        if file != new_file:
            os.system(f"cd {CACHE}; mv '{file}' '{new_file}'")

    # Move songs to given path
    print("Moving songs to given path..")
    os.system(f"mv {CACHE}/* {path}/ ; rmdir {CACHE}")
    

def collect_songs():

    ids = []

    print("Mention songs to downlaod, hit 'd' when done")
    while True:
        query = input(">> ")
        if query == 'd':
            break

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


if __name__ == "__main__":
    main()
