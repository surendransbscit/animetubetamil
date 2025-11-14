from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Channel, Anime, Season, Episode
from .serializers import ChannelSerializer, AnimeSerializer, SeasonSerializer, EpisodeSerializer


class ChannelAPIView(APIView):
    def get(self, request):
        channel = request.GET.get("channel")
        language = request.GET.get("language")

        channels = Channel.objects.all().order_by('created_on')

        if channel:
            channels = channels.filter(Q(name__icontains=channel))

        if language:
            channels = channels.filter(language=language)

        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimeAPIView(APIView):
    def get(self, request):
        anime = request.GET.get("anime")
        channel_id = request.GET.get("channel")

        animes = Anime.objects.select_related("channel").all()

        if anime:
            animes = animes.filter(name__icontains=anime)

        if channel_id:
            animes = animes.filter(channel_id=channel_id)

        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SeasonAPIView(APIView):
    def get(self, request):
        anime_id = request.GET.get("anime")
        season_number = request.GET.get("season")

        seasons = Season.objects.select_related("anime").all()

        if anime_id:
            seasons = seasons.filter(anime_id=anime_id)

        if season_number:
            seasons = seasons.filter(season_number=season_number)

        serializer = SeasonSerializer(seasons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EpisodeAPIView(APIView):
    def get(self, request):
        season_id = request.GET.get("season")
        min_ep = request.GET.get("min_ep")
        max_ep = request.GET.get("max_ep")

        episodes = Episode.objects.select_related("season", "season__anime").all()

        if season_id:
            episodes = episodes.filter(season_id=season_id)

        if min_ep:
            episodes = episodes.filter(episode_number__gte=min_ep)

        if max_ep:
            episodes = episodes.filter(episode_number__lte=max_ep)

        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "hello"})
