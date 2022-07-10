# Prerequisities
## Python
...

## yt-dlp

### Installation
You can install yt-dlp binary exexutable from [here](https://pypi.org/project/yt-dlp/#installation):

After installation, be sure to add yt-dlp to your system variable path. Try running yt-dlp in terminal to check
your installation

### Usage
yt-dlp [OPTIONS] [--] URL [URL...]

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
cd stocks
python3 -m venv venv
```
#### Windows
```cmd
cd stocks
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
### Set API key
#### Bash
```bash
export API_KEY=value
```
#### Command Prompt
```cmd
set API_KEY=value
```

## Run using
```bash
flask run
```






