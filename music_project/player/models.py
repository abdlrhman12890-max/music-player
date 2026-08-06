from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=100, unique=True)
    audio_file = models.FileField(upload_to='songs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title