from django.db.models import Q
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.timezone import now
from datetime import timedelta
from sport.models import (
    SportCategory, SportType, League, Team, 
    Player, Match, Standing, News
)


class Index(TemplateView):
    template_name = 'sports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters from GET
        sport_type = self.request.GET.get('sport_type', '')
        league = self.request.GET.get('league', '')
        level = self.request.GET.get('level', '')
        time_range = self.request.GET.get('time_range', 'today')  # today, week, month, all

        # Base querysets
        leagues_qs = League.objects.all()
        matches_qs = Match.objects.all()
        news_qs = News.objects.filter(is_headline=True)

        # Apply filters
        if sport_type:
            leagues_qs = leagues_qs.filter(sport_type__slug=sport_type)
            matches_qs = matches_qs.filter(league__sport_type__slug=sport_type)
            news_qs = news_qs.filter(related_sport__slug=sport_type)

        if league:
            matches_qs = matches_qs.filter(league__slug=league)
            news_qs = news_qs.filter(related_league__slug=league)

        if level:
            leagues_qs = leagues_qs.filter(level=level)
            matches_qs = matches_qs.filter(league__level=level)

        # Time-based filtering
        today = now().date()
        if time_range == 'today':
            matches_qs = matches_qs.filter(
                Q(match_date__date=today) |
                Q(match_date__date=today + timedelta(days=1))
            )
        elif time_range == 'week':
            matches_qs = matches_qs.filter(
                match_date__date__range=[today, today + timedelta(days=7)]
            )
        elif time_range == 'month':
            matches_qs = matches_qs.filter(
                match_date__date__range=[today, today + timedelta(days=30)]
            )

        # Matches
        live_matches = matches_qs.filter(status='live').select_related('home_team', 'away_team', 'league').order_by('match_date')
        upcoming_matches = matches_qs.filter(status='scheduled').select_related('home_team', 'away_team', 'league').order_by('match_date')[:10]
        recent_matches = matches_qs.filter(status='finished').select_related('home_team', 'away_team', 'league').order_by('-match_date')[:10]

        # Standings
        standings = Standing.objects.filter(league__in=leagues_qs).select_related('team', 'league').order_by('league', 'position')
        standings_by_league = {}
        for standing in standings:
            standings_by_league.setdefault(standing.league.name, []).append(standing)

        # Update context
        context.update({
            'categories': SportCategory.objects.all(),
            'sport_types': SportCategory.objects.values_list('sport_types__name', 'sport_types__slug').distinct(),
            'leagues': leagues_qs,
            'levels': League.LEVEL_CHOICES,
            'live_matches': live_matches,
            'upcoming_matches': upcoming_matches,
            'recent_matches': recent_matches,
            'standings_by_league': standings_by_league,
            'headlines': news_qs.order_by('-published_date')[:5],
            'selected_sport_type': sport_type,
            'selected_league': league,
            'selected_level': level,
            'selected_time_range': time_range,
        })

        return context