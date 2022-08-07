import glob
import music_tag
import os

from helpers import search_song, get_lyrics

songs = []

# Get songs one by one
print("Mention songs to downlaod, hit 'q' when done")
while True:

    query = input(">> ")
    if query in ['q', 'quit']:
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
    song = {
        'id' : results[0]['id'],
        'title': title
    }
    songs.append(song)


# Set download paths
path = input("Download Path: ") or '.'
if path.endswith('/'):
    path = path[:-1]

output_template = f"-o {path}/%(title)s.%(ext)s"

for song in songs:

    # Download song 
    os.system(f"yt-dlp {output_template} https://www.youtube.com/watch?v={song['id']}")

    # Get recently downloaded song file in the directory
    list_of_files = glob.glob(f'{path}/*.mp3') 
    latest_file = max(list_of_files, key=os.path.getctime)

    # Add lyrics 
    try:
        lyrics = get_lyrics(song['title'])
        data = music_tag.load_file(latest_file)
        data['lyrics'] = lyrics
        data.save()        
        
    except LyricScraperException:
        print("Lyrics not found!")
        continue


