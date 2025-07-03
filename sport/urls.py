from django.urls import path
from .views import (
    HomeView, CategoryDetailView, SportTypeDetailView, LeagueDetailView,
    TeamDetailView, PlayerDetailView, MatchDetailView, FixturesListView,
    ResultsListView, NewsListView, NewsDetailView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    # Category and sport type
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('sport/<slug:slug>/', SportTypeDetailView.as_view(), name='sport_type_detail'),
    
    # Leagues, teams, players
    path('league/<slug:slug>/', LeagueDetailView.as_view(), name='league_detail'),
    path('team/<slug:slug>/', TeamDetailView.as_view(), name='team_detail'),
    path('player/<slug:slug>/', PlayerDetailView.as_view(), name='player_detail'),
    
    # Matches
    path('match/<int:pk>/', MatchDetailView.as_view(), name='match_detail'),
    path('fixtures/', FixturesListView.as_view(), name='fixtures'),
    path('results/', ResultsListView.as_view(), name='results'),
    
    # News
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
]