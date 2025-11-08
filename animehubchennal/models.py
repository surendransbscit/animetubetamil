from django.db import models
from cloudinary.models import CloudinaryField

class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    LANGUAGE_CHOICES = (
        ("tamil", "Tamil"),
        ("english", "English"),
        ("hindi", "Hindi"),
        ("malayalam", "Malayalam"),
        ("telugu", "Telugu"),
    )
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "channels"

class Anime(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="animes")
    name = models.CharField(max_length=255)
    image = CloudinaryField("image", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "animes"


class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="seasons")
    season_number = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.anime.name} - Season {self.season_number}"
    
    class Meta:
        db_table = "seasons"

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    episode_number = models.PositiveIntegerField()
    youtube_link = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.season.anime.name} - Season {self.season.season_number} - Episode {self.episode_number}"

    class Meta:
        db_table = "episodes"
