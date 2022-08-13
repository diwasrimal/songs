# Prerequisites
## Python 3.6+

Since this is a Flask project. You must have python installed for this. Since I've used libraries that require newer python versions, I'd recommend you to install python with version 3.6+.

You can just head over to [Python download page](https://www.python.org/downloads/)

## sqlite3

I've used `sqlite` as my database in this project. 

You can head over to [sqlite downloads](https://www.sqlite.org/download.html) page and get the latest `sqlite3`.


## yt-dlp

**yt-dlp** is a youtube-dl fork based on the now inactive youtube-dlc. It lets you download videos and audios from YouTube with a lot of flexibility. It is a very powerful tool.


### Installation
You can install `yt-dlp` binary executable from [here](https://pypi.org/project/yt-dlp/#installation):

After installation, be sure to add `yt-dlp` to your system variable path. Try running yt-dlp in terminal to check
your installation

### Usage

You can read the [docs](https://github.com/yt-dlp/yt-dlp#readme) to get an understanding of most of the commands used in this project. The commands are in a config file in this project directory

`yt-dlp [OPTIONS] [--] URL [URL...]`

Some options beneficial for this project 

- `-x, --extract-audio`          
Convert video files to audio-only files
(requires ffmpeg and ffprobe)

- `--audio-format FORMAT`   
Select the format to download the current audio file
(currently supported: best (default),
`mp3`, `aac`, `m4a`, `opus`, `vorbis`, `flac`, `alac`,`wav`). You can specify multiple rules using
similar syntax as `--remux-video`

- `--audio-quality QUALITY`     
Specify ffmpeg audio quality to use when
converting the audio with `-x`. Insert a value
between 0 (best) and 10 (worst) for VBR or a
specific bit rate like 128K (default 5)   

- `--embed-thumbnail `  
Embed thumbnail in the audio or video as cover
art. Requires mutagen (Can be installed using `pip`) (sometimes ffmpeg may not be sufficient)



## FFmpeg  4.0 or newer:
[FFmpeg](https://ffmpeg.org/) is a free and open-source software project consisting of a suite of libraries and programs for handling video, audio, and other multimedia files and streams. At its core is the command-line ffmpeg tool itself, designed for processing of video and audio files.

Here in this project, we use ffmpeg to convert files downloaded using `yt-dlp` into music files. It converts media file extensions and is very helpful for downloading `.mp3` like file

Be sure to add `ffmpeg` to your path. Try executing `ffmpeg` command from your command line. Make sure it works



# Working

## `yt-dlp.conf`

We have to make a config file for yt-dlp that works specifically for this project. The file is named `yt-dlp.conf` and it directs the `yt-dlp` downloader how to download and convert music files.

Note that we'll only used `yt-dlp` executable for downloading songs locally. While running the web app, songs will be downloaded via `yt_dlp` python library.

## Database

Instead of messing with `sqlalchemy`, I have used `sqlite3` in this project to handle my database. I wanted it to be simple easy, thus sqlite would be better for this.

To manage the database queries, I have used the 'cs50' python module. It covers up all the unnecessary low level implementations and gives you that abstraction.

You can use `pip install cs50` to install `cs50` module. But don't worry, this included in  `requirements.txt` already

Making `SQL` queries using `cs50` module is very easy:

```py
from cs50 import SQL

# Configure database
db = SQL("sqlite:///songs.db")

# The db.execute() function is used to run sqlite queries
# It returns a list of dictionaries as a query result

# You can be straight forward and run queries like this
result = db.execute("SELECT * FROM songs WHERE id = ?", id)

```

## Embedding lyrics 

**[music-tag](https://github.com/KristoforMaynard/music-tag)** is a library for editing audio metadata with an interface that does not depend on the underlying file format. In other words, editing mp3 files should not be any different from `flac`, `m4a`, ... This library is just a layer on top of mutagen, which does all the heavy lifting.

`pip install music-tag`

This is included in `requirements.txt`, No need to worry!

If user wishes to download the song file, we give it in the form of mp3, embedding lyrics inside its metadata.

Some `music-tag` CLI commands:
```bash
# Set a couple of tags for multiple files      
python -m music_tag --set "genre:Pop" --set "comment:cli test" \
    ./sample/440Hz.aac ./sample/440Hz.flac

# Write tags from csv file to audio files (assuming file paths in
# the csv file are relative to the sample directory
python -m music_tag --from-csv tags.csv
```

However, we will be using the easier way here:

Embedding lyrics inside a song is as simple as:
```py
import music_tag

def embed_lyrics(song="path/to/song", lyrics="Twinkle Twinkle little star..."):
    data = music_tag.load_file("path/to/song")
    data['lyrics'] = lyrics
    data.save()

```

Looking embedded lyrics is much more easy
```py
import music_tag

def look_lyrics(song="path/to/song"):
    data = music_tag.load_file(song)
    return str(data['lyrics'])

```

## Getting lyrics

[**lyrics-extractor**](https://github.com/Techcatchers/PyLyrics-Extractor) is a python library which can be used to search for a song's lyrics

It fetches, extracts and returns the song's title and song lyrics from various websites, autocorrecting the song names for the misspelled names along the way.

`pip install lyrics-extractor`

### Requirements

You will need an API Key and Engine ID of Google Custom Search JSON API.

Create your new Custom Search Engine here to get your Engine ID: https://cse.google.com/cse/create/new

Add any of the following or all websites as per your choice in your Custom Search Engine:
- https://genius.com/
- http://www.lyricsted.com/
- http://www.lyricsbell.com/
- https://www.glamsham.com/
- http://www.lyricsoff.com/
- http://www.lyricsmint.com/

Get your API key here: https://developers.google.com/custom-search/v1/overview




### How to use
```Py
from lyrics_extractor import SongLyrics


extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)

data = extract_lyrics.get_lyrics("Shape of You")
```

## Downloading

All the audio files that are downloaded are stored inside `static/downloads/audio/`. Each song file has its own directory named by its id. 

#### Downloading locally

Note that I've also created a python file named `download.py` but have never imported or used it inside `app.py`. 

If you ever want to just download the songs locally and quickly without ever running the web app, you can use this python program. Just run `python download.py` in your terminal and you'll be prompted for inputs. This is a command line program I created for me to download songs as quickly as possible. I guessed it could be helpful for others too, so I added this to github.

# Configure and Run

Run the following scripts to configure your environment

### Make venv and install dependencies

- #### Windows users

```PS
python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt
```

- #### Linux/macOS users

```bash
python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt
```

## Fetching lyrics

Notice that you'll need a google custom programmable search engine to fetch lyrics using the `lyrics-extractor` module. Have a look [above](https://github.com/diwasrimal/Songs#getting-lyrics).

### Setup API key and engine ID

- #### Windows (PowerShell)
```powershell
$env:GCS_API_KEY = "your_key"
$env:GCS_ENGINE_ID = "your_id"
```

- #### Windows (cmd)
```cmd
set GCS_API_KEY=your_key
set GCS_ENGINE_ID=your_id
```

- #### macOS/Linux
```Bash
export GCS_API_KEY=your_key
export GCS_ENGINE_ID=your_id
```

## Run

After you activate your scripts, enter virtual environment and set up environment variables (api keys), you can just run the server by hitting 

```
flask run
```

## Use a script instead

I'd encourage anybody to use a script rather than typing these lines every time you run the application.

I've made a couple of scripts inside the `scripts/` directory. I've included PowerShell `.ps1` and Bash `.sh` scripts. 

### Configure script

- #### Windows users

Run `./scripts/configure.ps1` inside Windows PowerShell

```PS
# Create a virutal environment
python -m venv venv

.\venv\Scripts\activate

# installing project dependencies
pip install -r requirements.txt
```

- #### Linux/macOS users

run `./scripts/configure.sh` inside the bash shell
```bash
#!/bin/bash

echo "Creating a virutal env..."
python3 -m venv venv

. venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
```

Note: If you see something like `permission denied.`, just change the file mode and make it runnable. 

`chmod u+x ./scripts/configure.sh` and then `./scripts/run.sh`

### Runner scripts

Be sure to edit your environment variables before running these scripts. Replace the `your_key` and `your_id` with appropriate values.

- #### Windows users

Run `./scripts/run.ps1` inside Windows Powershell

```
# Set up flask environemt
.\venv\Scripts\activate

# Optional (For debugging)
# $env:FLASK_ENV = "development"

# Set Search engine ID:
$env:GCS_ENGINE_ID = "your_id"

# Set Custom Search JSON API Key : 
$env:GCS_API_KEY = "your_key"

# Run
flask run
```

- #### Linux/macOS users

run `./scripts/run.sh` inside your bash shell

```bash
#!/bin/bash

# Setup environment
. venv/bin/activate

# Optional (For debugging)
# export FLASK_ENV=development

# Set enviroment variables
export GCS_API_KEY=your_key
export GCS_ENGINE_ID=your_id

# Run the server
flask run
```


# Limitations/Improvements

Since I made this project as a beginner, there certainly are some things that can be improved. 

## Some limitations:

- A little slower download when song queried for first time
- Lyrics are scraped rather than being completely sourced.

## What can be improved here ?

- Song download and lyrics fetching could get faster while opening `/play` route

I tried this a lot, but I couldn't figure out a way to make these two processes concurrent. Since I'm using a library for fetching lyrics, this was a little complicated. I will complete this in the near future, but I am leaving this as it is right now.

- A page to show user's profile could be made

# Contributing

Of course, any contributions are welcome! 

- Fork this repository
- Clone it and make changes
- Test the changes
- Send a Pull Request
