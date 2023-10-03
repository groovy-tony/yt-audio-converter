from pytube import YouTube, Search
from yt_dlp import YoutubeDL, os
from youtube_search import YoutubeSearch
from moviepy.editor import AudioFileClip
from simple_term_menu import TerminalMenu
import glob


db_path = os.environ["HOME"] + "/Dropbox/YT Audio Files/"


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
    menu = TerminalMenu(
        ["Yes", "No"], title=f"Copy downloaded files to Dropbox? ({db_path})"
    )
    idx = menu.show()
    if idx:
        update_dropbox()


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


def update_dropbox():
    # get $HOME path and append Dropbox/YT \Audio file
    # move all .m4a files to it
    print(f"Copying downloaded files to {db_path}...")
    try:
        os.mkdir(db_path)
    except FileExistsError:
        pass
    for file in glob.glob("*.m4a"):
        print(file)
        os.replace(file, db_path + file)
    print("Done.")


def yt_search(query: str, max_results=None):
    if max_results is None:
        max_results = 10
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    titles = [
        f"{item['channel']} - {item['title']} - {item['duration']} - {item['publish_time']}"
        for item in results
    ]
    menu = TerminalMenu(titles)
    idx = menu.show()
    selection = results[idx]
    video_to_audio(f"https://www.youtube.com/watch?v={selection['id']}")


if __name__ == "__main__":
    update_dropbox()
    draw_menu()
    # video_to_audio("https://www.youtube.com/watch?v=jJPchQvTMhw")
