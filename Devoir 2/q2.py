import yt_dlp
import ffmpeg
import pandas as pd
import numpy as np
import csv
import threading
from tqdm import tqdm
from os.path import exists


def download_audio(YTID: str, path: str) -> None:
    """
    Create a function that downloads the audio of the Youtube Video with a given ID
    and saves it in the folder given by path. Download it as an mp3. If there is a problem downloading the file, handle the exception. If a file at `path` exists, the function should return without attempting to download it again.

    ** Use the library youtube_dl: https://github.com/ytdl-org/youtube-dl/ **
    Args:
      YTID: Contains the youtube ID, the corresponding youtube video can be found at
      'https://www.youtube.com/watch?v='+YTID
      path: The path to the file where the audio will be saved
    """

    URLS = ["https://www.youtube.com/watch?v=" + YTID]

    # These options are necessary since quality of audio is important during analysis
    options = {
      'format': 'bestaudio/best',
      'outtmpl' : path,
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }],
      'cookiefile': 'cookies.txt', # Chrome EditThisCookie extension in NETSCAPE format
      'extractor_args': {
        'youtube': {
            'player-client': 'web,default',
            'po_token': 'web+MnQa8aNfyTb0OhrJXIyLQfnkjJuus7C81-hnz8NqKGlvEJiiJmku2bK-taLvAhFgxC4dkZrtII3n6-guUJQgWojluPkI0VXh8Grp-rhpKVkcfkp2VRlcWMVsE-u4sayBdIFLE5kbaVq_DpUiItTua6DjiEMmIA==' # videoplayback pot parameter from an embbed video
        }
      }
    }

    try:
      if exists(path + ".mp3"):
         raise Exception("The audio file already exists.")

      with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(URLS)
    except Exception as e:
       print(e)


def cut_audio(in_path: str, out_path: str, start: float, end: float) -> None:
    """
    Create a function that cuts the audio from in_path to only include the segment from start to end and saves it to out_path.

    ** Use the ffmpeg library: https://github.com/kkroening/ffmpeg-python
    Args:
      in_path: Path of the audio file to cut
      out_path: Path of file to save the cut audio
      start: Indicates the start of the sequence (in seconds)
      end: Indicates the end of the sequence (in seconds)
    """

    input_audio = ffmpeg.input(in_path + ".mp3")
    filtered_audio = input_audio.filter('atrim', start=start, end=end)
    output_stream = ffmpeg.output(filtered_audio, out_path + ".mp3")

    output_stream.run()

if __name__ == "__main__":
    download_audio("Eq_FN9XTo3Q", "./data/input")
    cut_audio("./data/input", "./data/trimmed_input", 0, 10)