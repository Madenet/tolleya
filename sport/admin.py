from django.contrib import admin
from .models import (
    SportCategory, SportType, League, Team, 
    Player, Match, MatchEvent, Standing, News
)

class SportTypeInline(admin.TabularInline):
    model = SportType
    extra = 1

@admin.register(SportCategory)
class SportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SportTypeInline]

class LeagueInline(admin.TabularInline):
    model = League
    extra = 1

@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LeagueInline]

class TeamInline(admin.TabularInline):
    model = Team
    extra = 1

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type', 'level', 'country')
    list_filter = ('sport_type', 'level', 'country')
    search_fields = ('name', 'country')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TeamInline]

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'short_name')
    list_filter = ('league',)
    search_fields = ('name', 'short_name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlayerInline]

class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    extra = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date', 'status', 'league')
    list_filter = ('league', 'status', 'match_date')
    search_fields = ('home_team__name', 'away_team__name')
    date_hierarchy = 'match_date'
    inlines = [MatchEventInline]

@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'event_type', 'player', 'team', 'minute')
    list_filter = ('event_type', 'team', 'match__league')
    search_fields = ('player__first_name', 'player__last_name')

@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'position', 'played', 'points')
    list_filter = ('league',)
    ordering = ('league', 'position')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_headline', 'related_sport')
    list_filter = ('is_headline', 'related_sport', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'