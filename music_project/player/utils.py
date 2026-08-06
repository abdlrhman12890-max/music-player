import os
import yt_dlp
from django.conf import settings

def download_song_local(query):
    media_songs_dir = os.path.join(settings.MEDIA_ROOT, 'songs')
    os.makedirs(media_songs_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(media_songs_dir, '%(id)s.%(ext)s'),
        'ffmpeg_location': '/usr/bin',  # تحديد مكان ffprobe و ffmpeg المباشر
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'remote_components': ['ejs:github'],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]
            video_id = info['id']
            file_relative_path = f"songs/{video_id}.mp3"
            
            return {
                'id': video_id,
                'title': info['title'],
                'file_url': f"/media/songs/{video_id}.mp3",
                'relative_path': file_relative_path
            }
        except Exception as e:
            print("Error downloading audio:", e)
            return None