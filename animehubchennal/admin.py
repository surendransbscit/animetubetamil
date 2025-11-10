from django.contrib import admin
from .models import Channel, Anime, Season, Episode


# --- Episode Inline inside Season ---
class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ("episode_number", "youtube_link")
    ordering = ("episode_number",)


admin.site.index_title="AnimeTube Tamil"
admin.site.site_header="AnimeTube Tamil Dashboard"
admin.site.site_title ="AnimeTube Tamil"


# --- Season Inline inside Anime ---
class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    fields = ("season_number",)
    ordering = ("season_number",)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "language", "created_on", "updated_on")
    search_fields = ("name", "author")
    list_filter = ("language",)
    ordering = ("name", "language")
    readonly_fields = ("created_on", "updated_on")
    list_editable = ("name","author","language")


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("name", "channel", "created_on", "updated_on")
    search_fields = ("name", "channel__name")
    list_filter = ("channel__language",)
    ordering = ("channel", "name")
    readonly_fields = ("created_on", "updated_on")
    list_editable = ("name", "channel")
    inlines = [SeasonInline]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("anime", "season_number", "channel_name")
    raw_id_fields = ("anime",)
    search_fields = ("anime__name",)
    ordering = ("anime", "season_number")
    readonly_fields = ("created_on", "updated_on")
    inlines = [EpisodeInline]

    def channel_name(self, obj):
        return obj.anime.channel.name
    channel_name.short_description = "Channel Name"


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("anime_name", "season", "episode_number", "youtube_link", "channel_name", "created_on")
    raw_id_fields = ("season",)
    search_fields = ("season__anime__name",)
    ordering = ("season", "episode_number")
    readonly_fields = ("created_on", "updated_on")

    def channel_name(self, obj):
        return obj.season.anime.channel.name
    channel_name.short_description = "Channel Name"

    def anime_name(self, obj):
        return obj.season.anime.name
    anime_name.short_description = "Anime Name"
