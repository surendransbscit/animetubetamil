from rest_framework import serializers
from .models import Anime, Episode, Channel, Season

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class AnimeSerializer(serializers.ModelSerializer):
    channel = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all())
    channel_name = serializers.CharField(source='channel.name', read_only=True)

    class Meta:
        model = Anime
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=Anime.objects.all())
    anime_name = serializers.CharField(source='anime.name', read_only=True)
    channel_name = serializers.CharField(source='anime.channel.name', read_only=True)
    anime_img = serializers.ImageField(source='anime.image', read_only=True)

    class Meta:
        model = Season
        fields = '__all__'

class EpisodeSerializer(serializers.ModelSerializer):
    season = serializers.PrimaryKeyRelatedField(queryset=Season.objects.all())

    class Meta:
        model = Episode
        fields = '__all__'
