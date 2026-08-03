from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-to-playlist/', views.add_to_playlist, name='add_to_playlist'),
]