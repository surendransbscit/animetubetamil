import yt_dlp

def get_videos_from_playlist(playlist_url):
    """Return list of (title, url) for each video in a YouTube playlist"""
    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "dump_single_json": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    videos = []
    for entry in info.get("entries", []):
        video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
        videos.append((entry.get("title"), video_url))
    return videos
