from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('deepfakeimage', views.deepfakeimage, name='deepfakeimage'),
    path('deepfakeaudio', views.deepfakeaudio, name='deepfakeaudio')
]