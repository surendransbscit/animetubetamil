from django.contrib import admin, messages
from django import forms
from .models import Channel, Anime, Season, Episode
from utils.youtube_import import get_videos_from_playlist


# -----------------------------
# GLOBAL ADMIN CUSTOMIZATION
# -----------------------------
admin.site.index_title = "AnimeTube Tamil"
admin.site.site_header = "AnimeTube Tamil Dashboard"
admin.site.site_title = "AnimeTube Tamil"


# -----------------------------
# INLINE DEFINITIONS
# -----------------------------
class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    fields = ("season_number",)
    ordering = ("season_number",)


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0
    fields = ("episode_number", "youtube_link")
    readonly_fields = ("episode_number", "youtube_link")
    ordering = ("episode_number",)


# -----------------------------
# ADMIN: CHANNEL
# -----------------------------
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "language", "created_on", "updated_on")
    search_fields = ("name", "author")
    list_filter = ("language",)
    ordering = ("name",)
    readonly_fields = ("created_on", "updated_on")
    list_editable = ("author", "language",)
    list_per_page = 20


# -----------------------------
# ADMIN: ANIME
# -----------------------------
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("name", "channel", "created_on", "updated_on")
    search_fields = ("name", "channel__name")
    list_filter = ("channel__language",)
    ordering = ("channel", "name")
    readonly_fields = ("created_on", "updated_on")
    list_editable = ("channel",)
    list_per_page = 20
    inlines = [SeasonInline]


# -----------------------------
# ADMIN: SEASON
# -----------------------------
class SeasonImportForm(forms.ModelForm):
    playlist_url = forms.URLField(
        required=False,
        help_text="🎥 Enter a YouTube playlist URL to auto-import all episodes for this season.",
        label="YouTube Playlist URL"
    )

    class Meta:
        model = Season
        fields = "__all__"


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("anime", "season_number", "channel_name")
    list_filter = ("anime__channel__language", "anime__channel__name", "anime")
    search_fields = ("anime__name",)
    ordering = ("anime", "season_number")
    readonly_fields = ("created_on", "updated_on")
    list_per_page = 20
    inlines = [EpisodeInline]
    form = SeasonImportForm

    def channel_name(self, obj):
        return obj.anime.channel.name
    channel_name.short_description = "Channel Name"

    def save_model(self, request, obj, form, change):
        """When saving a Season, check for playlist URL and auto-create episodes."""
        super().save_model(request, obj, form, change)
        playlist_url = form.cleaned_data.get("playlist_url")

        if playlist_url:
            try:
                videos = get_videos_from_playlist(playlist_url)
                Episode.objects.filter(season=obj).delete()  # remove old episodes

                for i, (title, url) in enumerate(videos, start=1):
                    Episode.objects.create(
                        season=obj,
                        episode_number=i,
                        youtube_link=url,
                    )

                messages.success(
                    request, f"✅ Imported {len(videos)} episodes from playlist successfully!"
                )

            except Exception as e:
                messages.error(request, f"❌ Error while importing: {e}")


# -----------------------------
# ADMIN: EPISODE
# -----------------------------
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("anime_name", "season", "episode_number", "youtube_link", "channel_name", "created_on")
    raw_id_fields = ("season",)
    list_filter = ("season__anime__channel__language", "season__anime__channel__name", "season__anime__name")
    search_fields = ("season__anime__name",)
    ordering = ("season", "episode_number")
    readonly_fields = ("created_on", "updated_on")
    list_per_page = 20

    def channel_name(self, obj):
        return obj.season.anime.channel.name
    channel_name.short_description = "Channel Name"

    def anime_name(self, obj):
        return obj.season.anime.name
    anime_name.short_description = "Anime Name"
