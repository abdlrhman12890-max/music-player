import os
import yt_dlp
from django.conf import settings

def download_song_local(query):
    # إنشاء مجلد media/songs لو مش موجود
    media_songs_dir = os.path.join(settings.MEDIA_ROOT, 'songs')
    os.makedirs(media_songs_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(media_songs_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'js_runtimes': {
            'deno': {}
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]
            video_id = info['id']
            file_relative_path = f"songs/{video_id}.mp3"
            
            return {
                'id': video_id,
                'title': info['title'],
                'file_url': f"{settings.MEDIA_URL}{file_relative_path}",
                'relative_path': file_relative_path
            }
        except Exception as e:
            print("Error downloading audio:", e)
            return None