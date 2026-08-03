from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(unique=True)
    stream_url = models.URLField(blank=True,null=True)
    audio_file = models.FileField(upload_to='songs/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    # العلاقة بين الأغاني والقوائم (الأغنية الوحدة تنفع تكون في كذا قائمة، والقائمة فيها كذا أغنية)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name