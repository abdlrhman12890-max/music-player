from django.shortcuts import render, redirect
from .models import Song
from .utils import download_song_local

def index(request):
    query = request.GET.get('q')
    current_song = None

    if query:
        song_data = download_song_local(query)
        if song_data:
            song, created = Song.objects.get_or_create(
                youtube_id=song_data['id'],
                defaults={
                    'title': song_data['title'],
                    'audio_file': song_data['relative_path']
                }
            )
            current_song = song

    songs = Song.objects.all().order_by('-created_at')
    
    return render(request, 'player/index.html', {
        'songs': songs,
        'current_song': current_song
    })