from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('media/songs/<str:path>', views.serve_audio, name='serve_audio'),
]