import os
import sys

from platform import system
from helpers.songs import search_song

def main():

    usage = ('''Usage:
    python download.py -i                 (Interactive download) 
    python download.py -q song1 song2 ... (Quick download)
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

    # Set download paths
    path = input("Download path (default '~/Music/'): ") or '~/Music'
    if path.endswith('/'):
        path = path[:-1]

    # Download songs
    print("Starting download...\n")
    if system() == "Linux":
        output_template = f"-o {path}/%\\(title\\)s.%\\(ext\\)s"
    else:
        output_template = f"-o {path}/%(title)s.%(ext)s"
    for id in song_ids:
        os.system(f"yt-dlp {output_template} https://www.youtube.com/watch?v={id}")
        print()


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


if __name__ == "__main__":
    main()
