# Songs

Songs is a python project that lets you stream music online, or download the music locally.

### Video Demo: 
- https://www.youtube.com/watch?v=a-PEBQ6cv9Y

## Prerequisites

- [Python3.6+](https://www.python.org/downloads/)
- [SQLite3](https://www.sqlite.org/download.html) (database)
- [yt-dlp](https://pypi.org/project/yt-dlp/#installation) (video/audio downloader)
- [FFmpeg 4.0 or newer](https://ffmpeg.org)

Make these executable by adding to your global path.

## Quick run
To setup the project, you'll need to download the project requirements first.
Then you may set your environment and run the server.
- Clone the project
```sh
git clone https://github.com/diwasrimal/Songs.git
cd Songs
```

- Download requirements and make a virtual environment
 - If on **Windows**, run `./configure.ps1`
 - If on **Linux/macOS**, run `./configure.sh`
 
- Set [environment variables](https://github.com/diwasrimal/Songs#environment-variables)

- Then you can run the sever using `./run.sh` or `./run.ps1`


## Project Overview
```
.
├── app.py            : All your flask routes and functions
├── configure.ps1     
├── configure.sh
├── download.py       : Local download helper
├── helpers           : Additional functionalities
│   ├── lyrics.py
│   ├── songs.py
│   └── tools.py
├── music.db          : Database
├── README.md
├── requirements.txt  : Project requirements
├── run.ps1
├── run.sh
├── static            : Assets for front end
│   ├── css
│   ├── images
│   └── scripts
├── templates         : HTML pages
└── yt-dlp.conf       
```

### .sh and .ps1 scripts
Those scripts will help download dependencies, and set environment variables
while running a server.

### yt-dlp

The `yt-dlp.conf` file is a config file used by `yt-dlp`, the file is used to 
guide `yt-dlp` download our music.

### Database

Database is managed using `sqlite3` and a module `cs50`, which lets you make simpler
database queries.

An example database query using the `cs50` module
```py
from cs50 import SQL

# Configure database
db = SQL("sqlite:///songs.db")

# Query for a song with its id, gives back a dictionary
result = db.execute("SELECT * FROM songs WHERE id = ?", id)
```

### Embedding lyrics 

Embedding lyrics isn't a hassle, it is done using `music-tag`.

Its a library for editing audio metadata with an interface that does not depend on 
the underlying file format. In other words, editing mp3 files should not be any different 
from `flac`, `m4a`, ... This library is just a layer on top of mutagen, which does all the heavy lifting.

Here's how you embed lyrics using `music-tag`
```py
import music_tag

def embed_lyrics(song_file, lyrics):
    data = music_tag.load_file(song_file)
    data['lyrics'] = lyrics
    data.save()

embed_lyrics("~/Music/Twinkle.mp3", "Twinkle Twinkle Little Star, How I wonder what you are?")
```

Looking at the embedded lyrics is easier
```py
import music_tag

def look_lyrics(song_file):
    data = music_tag.load_file(song_file)
    return str(data['lyrics'])

lyrics = look_lyrics("~/Music/Twinkle.mp3")
```

### Getting lyrics

[**lyrics-extractor**](https://github.com/Techcatchers/PyLyrics-Extractor) is a python 
library which can be used to search for a song's lyrics.

It fetches, extracts and returns the song's title and song lyrics from various 
websites, autocorrecting the song names for the misspelled names along the way.

#### Environment Variables

For fetching lyrics, you'll need an **API key** and **Engine ID** 
of [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview).
You can watch the [video above](https://github.com/diwasrimal/Songs#video-demo) once

1. Create your new search engine and get **Engine ID**

2. Add any or all of the following websites in your custom search engine:
  - https://genius.com/
  - http://www.lyricsted.com/
  - http://www.lyricsbell.com/
  - https://www.glamsham.com/
  - http://www.lyricsoff.com/
  - http://www.lyricsmint.com/

3. Get your **API key**

4. Set environment variables while running the server, or set them in `run.sh` or `run.ps1`

   - Windows PowerShell
   ```powershell
   $env:GCS_API_KEY = "your_key"
   $env:GCS_ENGINE_ID = "your_id"
   ```
   - Linux/macOS
   ```sh
   export GCS_API_KEY=your_key
   export GCS_ENGINE_ID=your_id
   ```

An example fetching lyrics using our search engine and `lyrics-extractor`
```Py
import os
from lyrics_extractor import SongLyrics

GCS_API_KEY = os.environ.get("GCS_API_KEY")
GCS_ENGINE_ID = os.environ.get("GCS_ENGINE_ID")

extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)
data = extract_lyrics.get_lyrics("Shape of You")
```

### Downloading 

All the audio files that are downloaded from the server are stored inside `static/downloads/audio/`. 
Each song file has its own directory named by its id. Note that songid is the youtube videoid of 
the same song

#### Downloading Locally

Here's how you can download songs locally
```sh
$ python download.py
Usage:
    python download.py -q song1 song2 youtube-link ... (Quick download)
    python download.py -i                              (Interactive download)

$
```

### Project limitations:

- A little slower download when song queried for first time
- Lyrics are scraped rather than being completely sourced.

### What to improve ?

- Faster downloads?, I'm not sure.
- A page to show user's profile could be made

## Contributing

Of course, any contributions are welcome! 

- Fork this repository
- Make changes
- Test changes
- Send a Pull Request
