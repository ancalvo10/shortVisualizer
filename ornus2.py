import yt_dlp

url = "https://www.youtube.com/@ornuS2/shorts"

ydl_opts = {
    "quiet": True,
    "extract_flat": False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)

print("Entries:", len(info["entries"]))

ids = []

for entry in info["entries"]:
    print(entry.keys())     # temporal para inspeccionar
    ids.append(entry["id"])

print("IDs:", len(ids))

print("Playlist URL:")
print("https://www.youtube.com/watch_videos?video_ids=" + ",".join(ids))