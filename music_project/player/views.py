import os
import re
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
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

# دالة خدمة بث الصوت للموبايل بوضع Range Request (HTTP 206)
def serve_audio(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, 'songs', path)
    if not os.path.exists(file_path):
        raise Http404("File not found")

    file_size = os.path.getsize(file_path)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte)
        last_byte = int(last_byte) if last_byte else file_size - 1
        if last_byte >= file_size:
            last_byte = file_size - 1
        length = last_byte - first_byte + 1

        with open(file_path, 'rb') as f:
            f.seek(first_byte)
            data = f.read(length)

        response = HttpResponse(data, status=206, content_type='audio/mpeg')
        response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(length)
        return response
    else:
        with open(file_path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='audio/mpeg')
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes'
        return response