from pytube import YouTube, Search
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from moviepy.editor import AudioFileClip
from simple_term_menu import TerminalMenu


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
    yt_dlp_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }

    with YoutubeDL(yt_dlp_opts) as ydl:
        info = ydl.extract_info(url)
        error = ydl.download(url)


def yt_search(query: str, results=None):
    results = YoutubeSearch(query, max_results=10).to_dict()
    titles = [item['title'] for item in results]
    menu = TerminalMenu(titles)
    idx = menu.show()
    selection = results[idx]
    video_to_audio(f"https://www.youtube.com/watch?v={selection['id']}")


if __name__ == "__main__":
    draw_menu()
    # video_to_audio("https://www.youtube.com/watch?v=jJPchQvTMhw")
