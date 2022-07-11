# Prerequisities
## Python 3.6+
...

## yt-dlp

### Installation
You can install yt-dlp binary exexutable from [here](https://pypi.org/project/yt-dlp/#installation):

After installation, be sure to add yt-dlp to your system variable path. Try running yt-dlp in terminal to check
your installation

### Usage
`yt-dlp [OPTIONS] [--] URL [URL...]`

Some options beneficial for this project 

`-x, --extract-audio`          
Convert video files to audio-only files
(requires ffmpeg and ffprobe)

`--audio-format FORMAT`           
Format to convert the audio to when -x is
used. (currently supported: best (default),
mp3, aac, m4a, opus, vorbis, flac, alac,
wav). You can specify multiple rules using
similar syntax as --remux-video

`--audio-quality QUALITY`
Specify ffmpeg audio quality to use when
converting the audio with -x. Insert a value
between 0 (best) and 10 (worst) for VBR or a
specific bitrate like 128K (default 5)   

`--embed-thumbnail `
Embed thumbnail in the audio or video as cover
art. Requires mutagen (Can be installed using `pip`) (sometimes ffmpeg may not be sufficient)


## FFmpeg  4.0 or newer:
[FFmpeg](https://ffmpeg.org/) is a free and open-source software project consisting of a suite of libraries and programs for handling video, audio, and other multimedia files and streams. At its core is the command-line ffmpeg tool itself, designed for processing of video and audio files.

Here in this project, we use ffmpeg to convert files downloaded using yt-dlp into music files. It convert media file extensions and is very helpful for donwlading .mp3 like file


# Configuration

## Making a config file for yt-dlp

We have to make a config file for yt-dlp that works specifically for this project. The file is named `yt-dlp.conf` and it directs the yt-dlp downloader how to download and convert music files

## Configure Flask

### Set up a virtual environment
#### macOS/Linux
```bash
cd songs
python3 -m venv venv
```
#### Windows
```cmd
cd songs
python3 -m venv venv
```
### Run Scripts

#### macOS/Linux
```bash
. venv/bin/activate
```
#### Windows
```cmd
venv\Scripts\activate

```
### Install Flask
```bash
pip install Flask
```

### Install project requirements
```bash
pip install -r requirements.txt
```

# Working

## Embedding lyrics 

**[music-tag](https://github.com/KristoforMaynard/music-tag)** is a library for editing audio metadata with an interface that does not depend on the underlying file format. In other words, editing mp3 files shouldn not be any different than flac, m4a, ... This library is just a layer on top of mutagen, which does all the heavy lifting.

`pip install music-tag`

This is included in `requirements.txt`, No need to worry!

If user wishes to download the song file, we give it in the form of mp3 embedding lyrics inside its metadata.

some music-tag CLI commands:
```bash
# Set a couple tags for multiple files      
python -m music_tag --set "genre:Pop" --set "comment:cli test" \
    ./sample/440Hz.aac ./sample/440Hz.flac

# Write tags from csv file to audio files (assuming file paths in
# the csv file are relative to the sample directory
python -m music_tag --from-csv tags.csv
```

## Getting lyrics

[**lyrics-extractor**](https://github.com/Techcatchers/PyLyrics-Extractor) is a python library which can be used to search for a song's lyrics

It fetches, extracts and returns the song's title and song lyrics from various websites autocorrecting the song names for the misspelled names along the way.

`pip install lyrics-extractor`

### Requirements

    You will need an API Key and Engine ID of Google Custom Search JSON API.

        Create your new Custom Search Engine here to get your Engine ID: https://cse.google.com/cse/create/new

        Add any of the following or all websites as per your choice in your Custom Search Engine:
            https://genius.com/
            http://www.lyricsted.com/
            http://www.lyricsbell.com/
            https://www.glamsham.com/
            http://www.lyricsoff.com/
            http://www.lyricsmint.com/

        Get your API key here: https://developers.google.com/custom-search/v1/overview


### Setup API key and engine id
#### MacOS/Linux
```Bash
export GCS_API_KEY=AIzaSyBvnH37Vki63LwDty_MkmVQBIJEWDs1yaA
export GCS_ENGINE_ID=328400a11a17edf75
```

#### Windows
```cmd
set GCS_API_KEY=AIzaSyBvnH37Vki63LwDty_MkmVQBIJEWDs1yaA
set GCS_ENGINE_ID=328400a11a17edf75
```

#### Windows (Powershell)
```powershell
$env:GCS_ENGINE_ID = "328400a11a17edf75"
$env:GCS_API_KEY = "AIzaSyBvnH37Vki63LwDty_MkmVQBIJEWDs1yaA"
```


### How to use
```Py
from lyrics_extractor import SongLyrics

extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)

data = extract_lyrics.get_lyrics("Shape of You")
```




