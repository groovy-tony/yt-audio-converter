from pytube import YouTube, Search
from moviepy.editor import AudioFileClip
import os


def video_to_audio(url):
    yt = YouTube(
        url,
        # on_progress_callback=progress_func,
        # on_complete_callback=complete_func
    )
    video = yt.streams.get_audio_only().download(
        output_path="YT Audio Files/", filename_prefix=f"{yt.author} - "
    )

    audio = AudioFileClip(video)
    audio.write_audiofile(f'{video.split(".")[0]}.mp3')

    os.remove(video)


if __name__ == "__main__":
    video_to_audio("https://www.youtube.com/watch?v=jJPchQvTMhw")
