from yt_dlp import YoutubeDL, os
from youtube_search import YoutubeSearch
from simple_term_menu import TerminalMenu
import glob
import pprint

directory = "Library"
db_path = f"{os.environ['HOME']}/Dropbox/"


def draw_menu():
    keep_running = True
    while keep_running:
        options = [
            "Enter a YouTube URL",
            "Search YouTube",
            "Enter Playlist or Channel URL",
            "Sync to Dropbox",
            "Exit",
        ]
        menu = TerminalMenu(options, title="YouTube Audio Downloader")
        idx = menu.show()
        match idx:
            case 0:
                video_to_audio(input("Enter URL:\n"))
            case 1:
                yt_search(input("Enter search query:\n"))
            case 2:
                dl_playlist(
                    # "https://www.youtube.com/playlist?list=PLKn4Z-msM-9J4gIaaXMs8l-Jr0MW5ySTR"  # Vormithrax
                    # "https://www.youtube.com/channel/UCx2bHtrpvAW5tt72GAi0ULQ"  # The Jeffster
                    "https://www.youtube.com/watch?v=1lwDO1HUL1M&list=PLN0q19AZLbSd4epwHZYIsW4gqFUkHyhOd"  # Polyphia - The Most Hated
                    # "https://www.youtube.com/watch?v=83YDGKp3Ui0&list=PLKn4Z-msM-9JdzOCYsIVuAyciRaQ6BejC"
                )
            case 3:
                update_dropbox()
                exit()
            case 4:
                keep_running = False

        menu = TerminalMenu(
            ["Yes", "No"], title=f"Copy downloaded files to Dropbox? ({db_path})"
        )
        idx = menu.show()
        if not idx:
            update_dropbox()


def dl_playlist(url: str):
    """
    Downloads the audio from each video in a YouTube playlist or channel.
    Will skip any videos that have already been downloaded i.e. added to archive.txt.

    Args:
        url: URL of YouTube channel or playlist
    """
    yt_dlp_opts = {
        "download_archive": "archive.txt",
        "extract_flat": "discard_in_playlist",
        # "forcejson": True,
        "fragment_retries": 10,
        "ignoreerrors": "only_download",
        "overwrites": False,
        "format": "m4a/bestaudio/best",
        "outtmpl": {"default": "Library/%(uploader)s - %(title)s.%(ext)s"},
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
        "quiet": True,
        "retries": 10,
        "simulate": False,
    }

    with YoutubeDL(yt_dlp_opts) as ydl:
        # TODO: this extracts video info twice, maybe figure out another way to determine error state
        info = ydl.extract_info(url, download=False)
        error = ydl.download(url)
        # pprint.pprint(info)
        print("--- Downloading playlist... ---")
        print(info["title"])
        print(info["uploader"])
        print(info["webpage_url"])
        if not error:
            for x in info["entries"]:
                print(x["title"])
                print(type(x))


def video_to_audio(url: str):
    yt_dlp_opts = {
        "format": "m4a/bestaudio/best",
        "outtmpl": {"default": directory + "/%(uploader)s - %(title)s.%(ext)s"},
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }

    with YoutubeDL(yt_dlp_opts) as ydl:
        info = ydl.extract_info(url)
        # error = ydl.download(url)


def update_dropbox():
    # get $HOME path and append Dropbox/YT \Audio file
    # move all .m4a files to it
    print(f"Copying downloaded files to {db_path}...")
    try:
        os.mkdir(db_path)
    except FileExistsError:
        pass
    for file in glob.glob("Library/*.m4a"):
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
    # update_dropbox()
    draw_menu()
    # video_to_audio("https://www.youtube.com/watch?v=jJPchQvTMhw")
