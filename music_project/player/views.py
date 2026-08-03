from django.shortcuts import render, redirect
from .models import Song, Playlist
from .utils import get_video_info

def index(request):
    query = request.GET.get('q')
    searched_song = None

    if query:
        # 1. بنجيب بيانات الأغنية من يوتيوب الأول
        yt_data = get_video_info(query)
        
        if yt_data:
            # 2. نستخدم get_or_create بناءً على الـ youtube_id الفريد
            searched_song, created = Song.objects.get_or_create(
                youtube_id=yt_data['id'],
                defaults={
                    'title': yt_data['title'],
                    'stream_url': yt_data['stream_url'],
                }
            )

    all_songs = Song.objects.all().order_by('-created_at')
    playlists = Playlist.objects.all()

    context = {
        'searched_song': searched_song,
        'all_songs': all_songs,
        'playlists': playlists,
        'query': query,
    }
    return render(request, 'index.html', context)

def add_to_playlist(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        playlist_id = request.POST.get('playlist_id')
        new_playlist_name = request.POST.get('new_playlist_name')

        if song_id:
            song = Song.objects.get(id=song_id)

            # 1. لو كتب اسم قائمة جديدة، ننشئها
            if new_playlist_name and new_playlist_name.strip():
                playlist = Playlist.objects.create(name=new_playlist_name.strip())
                playlist.songs.add(song)

            # 2. لو اختر قائمة موجودة من الـ Dropdown
            elif playlist_id:
                playlist = Playlist.objects.get(id=playlist_id)
                playlist.songs.add(song)

    return redirect('index')