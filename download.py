import sys
import re
import yt_dlp
from pathlib import Path
from helpers.songs import search_song

DEBUG_MODE = True
LINK_PATTERN = r'^https://(?:www\.)?youtu\.?be(?:\.com)?/(?:watch\?v=)?(.*)'

def main():
    usage = ('''Usage:
    python download.py -q song1 song2 yt-link ... (Quick download)
    python download.py -f filename                (Download from file)
    python download.py -i                         (Interactive download) 
    ''')
    if len(sys.argv) < 2:
        sys.exit(usage)

    method = sys.argv[1]
    ids = []

    # Interactive selection of songs
    if method == '-i':
        ids = collect_ids_interactively()

    # Quick download (Gets queries from command line)
    elif method == '-q':
        queries = sys.argv[2:]
        if not queries:
            sys.exit(usage)

        print("Searching...")
        for i, query in enumerate(queries):
            if DEBUG_MODE:
                print("DEBUG: Item", i, query)

            if matches := re.search(LINK_PATTERN, query):
                if DEBUG_MODE:
                    print("DEBUG: Matches a link")
                ids.append(matches.group(1))
                continue

            results = search_song(query)
            if not results:
                print(f"{query} not found, skipping..")
                continue
            ids.append(results[0]['id'])

    # Load queries from file then download
    elif method == '-f':
        if len(sys.argv) != 3:
            sys.exit(usage)

        file = sys.argv[2]
        if DEBUG_MODE:
            print(f"DEBUG: Reading from file: {file}")
        if not file or not Path(file).exists():
            sys.exit("File not found!")

        print("Searching...")
        with open(file) as f:
            for i, query in enumerate(f):
                query = query.strip()
                if not query:
                    continue
                if DEBUG_MODE: 
                    print("DEBUG: Item", i, query)

                if matches := re.search(LINK_PATTERN, query):
                    if DEBUG_MODE:
                        print("DEBUG: Matches a link")
                    ids.append(matches.group(1))
                    continue

                results = search_song(query)
                if not results:
                    print(f"{query} not found, skipping..")
                    continue
                ids.append(results[0]['id'])

    if len(ids) == 0:
        sys.exit("No songs to download!")

    print(f"{len(ids)} ready to download.")

    # Download on a temp dir first, then move downloaded files
    tmp_dir = "./tmp"
    target_dir = input("Download dir (default: ~/Music): ") or "~/Music"

    downloaded = download_songs(ids, tmp_dir)
    if downloaded > 0:
        move_files(tmp_dir, target_dir)

    print(f"{len(ids)} tried to download, {downloaded} downloaded.")


def collect_ids_interactively():
    print("Enter songs/links, hit 'd' when done")
    ids = []
    while True:
        query = input(">> ")
        if query == 'd': 
            break
        if matches := re.search(LINK_PATTERN, query):
            if DEBUG_MODE:
                print("DEBUG: Matches a link")
            ids.append(matches.group(1))
            continue
        results = search_song(query)
        for result in results:
            response = input(f"{result['title']}? (y:yes, n:next, s:skip) ").strip()
            if response == 'y':
                ids.append(result['id'])
            elif response == 'n':
                continue
            break
        else:
            print("End of results, skipping..")
    return ids


def download_songs(song_ids, target_dir):
    """Downloads songs given their id/links"""
    if not song_ids:
        sys.exit("No song id/link found!")
    if DEBUG_MODE:
        print(f"DEBUG: Downloading: {song_ids}")

    # Use best quality and download as mp3 to given directory
    ydl_opts = { 
        'outtmpl': f'{target_dir}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'verbose': DEBUG_MODE,
        'writethumbnail': 'true',
        'postprocessors': [
            { 'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': 0, }, 
            { 'key': 'FFmpegMetadata', 'add_metadata': True, }, 
            { 'key': 'EmbedThumbnail', 'already_have_thumbnail': False, }
        ], 
    }

    downloaded = 0
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, song_id in enumerate(song_ids):
            try:
                url = f'https://youtube.com/watch?v={song_id}'
                error_code = ydl.download(url)
                downloaded += 1
                if DEBUG_MODE:
                    print(f"DEBUG: Error code for item {i}: {error_code}")
            except Exception:
                if DEBUG_MODE:
                    print()

    return downloaded


def move_files(source_dir, target_dir):
    source_dir = Path(source_dir).expanduser()
    target_dir = Path(target_dir).expanduser()

    if not target_dir.is_dir():
        target_dir.mkdir(parents=True)

    for file in source_dir.iterdir():
        file.rename(target_dir / file.name)
        print(file, '->', target_dir / file.name)


if __name__ == "__main__":
    main()
