from pytube import YouTube, Search
from moviepy.editor import AudioFileClip
from simple_term_menu import TerminalMenu
import os
import sys


def draw_menu():
    options = ["Enter a YouTube URL", "Search YouTube", "Enter YouTube Playlist"]
    menu = TerminalMenu(options, title="YouTube Audio Downloader")
    idx = menu.show()
    match idx:
        case 0:
            video_to_audio(input("Enter URL:\n"))
        case 1:
            yt_search(input("Enter search query:\n"))
        case 2:
            raise NotImplementedError


def video_to_audio(url: str):
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


def yt_search(query: str, results=None):
    src = Search(query)
    if results is None:
        results = src.results
    titles = []
    for r in results:
        titles.append(f"{r.author} - {r.title}")
    titles.append("--- Show More Results ---")
    menu = TerminalMenu(titles, title="Search results:")
    idx = menu.show()
    if idx == len(results):
        src.get_next_results()
        yt_search(query, results)

    video_to_audio(results[idx].watch_url)


if __name__ == "__main__":
    draw_menu()
    # video_to_audio("https://www.youtube.com/watch?v=jJPchQvTMhw")
