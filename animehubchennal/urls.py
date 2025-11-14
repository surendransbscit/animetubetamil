from django.urls import path
from .views import ChannelAPIView, AnimeAPIView, SeasonAPIView, EpisodeAPIView,HelloView

urlpatterns = [
    path("channels/", ChannelAPIView.as_view()),
    path("animes/", AnimeAPIView.as_view()),
    path("seasons/", SeasonAPIView.as_view()),
    path("episodes/", EpisodeAPIView.as_view()),
    path("home/",HelloView.as_view()),
]
