ytdl prerequisities


ffmpg  4.0 or newer:
[FFmpeg](https://ffmpeg.org/) is a free and open-source software project consisting of a suite of libraries and programs for handling video, audio, and other multimedia files and streams. At its core is the command-line ffmpeg tool itself, designed for processing of video and audio files.



Get your YT api key
https://developers.google.com/youtube/registering_an_application


Read more about YTDL at 
https://pypi.org/project/ytdl/
Config

- install pipx



There are 2 properties to configure: api_key and store_dir. At the first time, api_key is empty and you have to set it before using other features.

# set new `api_key`
ytdl config api_key YOUR_OWN_YOUTUBE_API_KEY

# change `store_dir` to new path
ytdl config store_dir /storage/downloads/youtube

# get the current value of `api_key`
ytdl config api_key

# show all
ytdl config

By default, store_dir is being set to /home/{YOUR_USER_NAME}/ytdl_files, you should change it to more appropriate place.


# yt-dlp
## Installation
You can install yt-dlp binary exexutable from [here](https://pypi.org/project/yt-dlp/#installation):

After installation, be sure to add yt-dlp to your system variable path. Try running yt-dlp in terminal to check
your installation

## Usage
yt-dlp [OPTIONS] [--] URL [URL...]

Some options beneficial for this project 
-x, --extract-audio             Convert video files to audio-only files
                                (requires ffmpeg and ffprobe)
--audio-format FORMAT           Format to convert the audio to when -x is
                                used. (currently supported: best (default),
                                mp3, aac, m4a, opus, vorbis, flac, alac,
                                wav). You can specify multiple rules using
                                similar syntax as --remux-video
--audio-quality QUALITY         Specify ffmpeg audio quality to use when
                                converting the audio with -x. Insert a value
                                between 0 (best) and 10 (worst) for VBR or a
                                specific bitrate like 128K (default 5)                  

## Making a config file

We have to make a config file for yt-dlp that works specifically for this project
