import innertube
import yt_dlp

# Searches for a song and gives back their ids, thumbnails ..
def search_song(q):
    client = innertube.InnerTube("WEB")
    data = client.search(q)

    # Retrieve list of useful searches
    contents = (data['contents']['twoColumnSearchResultsRenderer']['primaryContents']
		    ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'])
    data = []

    # Loop through some portion of contents and collect info
    for i in range(len(contents)):

        try:
            videoContent = contents[i]["videoRenderer"]
        except KeyError:
            continue

        thumbnail = videoContent["thumbnail"]["thumbnails"]
        data.append(
            {
                "id": videoContent["videoId"],
                # 'thumbnail': {
                # 	'url': thumbnail[0]['url'],
                # 	'width': thumbnail[0]['width'],
                # 	'height': thumbnail[0]['height']
                # },
                "thumbnail": thumbnail[0]["url"],
                "title": videoContent["title"]["runs"][0]["text"],
                "channel": videoContent["ownerText"]["runs"][0]["text"],
            }
        )

    return data


def download_song(path, song_id):

    URL = f'https://www.youtube.com/watch?v={song_id}'

    ydl_opts = {

        # Audio download format
        'format': 'm4a/bestaudio/best',

        # Output template for downloaded song
        'outtmpl': {
            'default': f'{path}/%(title)s.%(ext)s',
            'thumbnail': 'thumbnail'        # Embeds thumbnail (Not working)
        },

        # Extract audio to mp3 format using ffmpeg
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)
