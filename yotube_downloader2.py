import csv
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import PySimpleGUI as sg
from pytube import YouTube

def Download(link, title):
    # create a videos folder
    Path('Videos/').mkdir(parents=True, exist_ok=True)
    # create a temp folder
    Path('temp/').mkdir(parents=True, exist_ok=True)

    # check if the string exist in the link
    if "https://www.youtube.com/watch?v=" in link:
        print(
            f"Downloading Started for Video with title {title.strip()} \n")

        # Ceate Youtube Object
        youtubeObject = YouTube(link)

        try:
            # Youtube maintains Separate video and audio files for high resolution videos
            # download Video in a temp location
            youtubeObject.streams.get_highest_resolution().download(
                output_path="temp/", filename='video.mp4')

            # Download Audio in a temp location
            youtubeObject.streams.filter(abr="160kbps", progressive=False).first(
            ).download(output_path="temp/", filename='audio.mp3')

        except Exception as e:
            print(e)
            print("An error has occurred")
            sys.exit(1)

        # Access the Audio and video file location
        audio = "./temp/audio.mp3"
        video = "./temp/video.mp4"

        # Define the final merged video Location
        filepath = f"Videos/{title.strip().replace(' ','_')}.mp4"

        # Run FFmpeg in cmd to the audio and video format. this method is used as it is the fastest way to merge the files.
        cmd = f'ffmpeg -y -i {audio}  -r 30 -i {video}  -filter:a aresample=async=1 -c:a flac -c:v copy {filepath} -loglevel quiet -stats'
        subprocess.check_call(shlex.split(cmd))

        # deleting the temp folder
        shutil.rmtree("temp/")

    else:
        print("Invalid URL")

if __name__ == '__main__':
    Download("https://www.youtube.com/watch?v=YFmV_MRSD7M","测试")