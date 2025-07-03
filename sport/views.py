from django.db.models import Q
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import (
    SportCategory, SportType, League, Team, 
    Player, Match, Standing, News
)

class SportsDashboardView(TemplateView):
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

        # Time-based filtering for matches
        now = datetime.now()

        if time_range == 'today':
            matches_qs = matches_qs.filter(
                Q(match_date__date=now.date()) |
                Q(match_date__date=now.date() + timedelta(days=1))
            )
        elif time_range == 'week':
            matches_qs = matches_qs.filter(
                match_date__range=[now.date(), now.date() + timedelta(days=7)]
            )
        elif time_range == 'month':
            matches_qs = matches_qs.filter(
                match_date__range=[now.date(), now.date() + timedelta(days=30)]
            )

        # Organize matches
        live_matches = matches_qs.filter(status='live').select_related(
            'home_team', 'away_team', 'league'
        ).order_by('match_date')

        upcoming_matches = matches_qs.filter(status='scheduled').select_related(
            'home_team', 'away_team', 'league'
        ).order_by('match_date')[:10]

        recent_matches = matches_qs.filter(status='finished').select_related(
            'home_team', 'away_team', 'league'
        ).order_by('-match_date')[:10]

        # Standings
        standings = Standing.objects.filter(
            league__in=leagues_qs
        ).select_related('team', 'league').order_by('league', 'position')

        # Group standings by league
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

#homevview        
class HomeView(ListView):
    template_name = 'sports/index.html'
    context_object_name = 'headlines'

    def get_queryset(self):
        return News.objects.filter(is_headline=True).order_by('-published_date')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = SportCategory.objects.all()
        context['upcoming_matches'] = Match.objects.filter(status='scheduled').order_by('match_date')[:5]
        return context


#category
class CategoryDetailView(DetailView):
    model = SportCategory
    template_name = 'sports/category.html'
    context_object_name = 'category'
    slug_field = 'slug'


#sports
class SportTypeDetailView(DetailView):
    model = SportType
    template_name = 'sports/sport_type.html'
    context_object_name = 'sport_type'
    slug_field = 'slug'


#Leagure
class LeagueDetailView(DetailView):
    model = League
    template_name = 'sports/league.html'
    context_object_name = 'league'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = self.object
        context['standings'] = Standing.objects.filter(league=league).order_by('position')
        context['upcoming_matches'] = Match.objects.filter(league=league, status='scheduled').order_by('match_date')[:5]
        context['recent_matches'] = Match.objects.filter(league=league, status='finished').order_by('-match_date')[:5]
        context['news'] = News.objects.filter(related_league=league).order_by('-published_date')[:5]
        return context


#template
class TeamDetailView(DetailView):
    model = Team
    template_name = 'sports/team.html'
    context_object_name = 'team'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        context['players'] = Player.objects.filter(team=team).order_by('jersey_number')
        context['upcoming_matches'] = Match.objects.filter(
            models.Q(home_team=team) | models.Q(away_team=team),
            status='scheduled'
        ).order_by('match_date')[:5]
        context['recent_matches'] = Match.objects.filter(
            models.Q(home_team=team) | models.Q(away_team=team),
            status='finished'
        ).order_by('-match_date')[:5]
        context['news'] = News.objects.filter(related_team=team).order_by('-published_date')[:5]
        return context


#player details
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'sports/player.html'
    context_object_name = 'player'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.object
        context['news'] = News.objects.filter(related_player=player).order_by('-published_date')[:5]
        context['match_events'] = MatchEvent.objects.filter(player=player).select_related('match').order_by('-match__match_date')[:10]
        return context


#match details
class MatchDetailView(DetailView):
    model = Match
    template_name = 'sports/match_detail.html'
    context_object_name = 'match'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.object
        context['events'] = MatchEvent.objects.filter(match=match).order_by('minute')
        context['news'] = News.objects.filter(
            models.Q(related_team=match.home_team) | 
            models.Q(related_team=match.away_team) |
            models.Q(related_league=match.league)
        ).order_by('-published_date')[:3]
        return context

#fixtures list
# fixtures and list
class FixturesListView(ListView):
    model = Match
    template_name = 'sports/fixtures.html'
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        level = self.request.GET.get('level', None)
        sport_type = self.request.GET.get('sport_type', None)
        league = self.request.GET.get('league', None)
        team = self.request.GET.get('team', None)
        
        queryset = Match.objects.filter(status='scheduled').order_by('match_date')
        
        if level:
            queryset = queryset.filter(league__level=level)
        if sport_type:
            queryset = queryset.filter(league__sport_type__slug=sport_type)
        if league:
            queryset = queryset.filter(league__slug=league)
        if team:
            queryset = queryset.filter(
                models.Q(home_team__slug=team) | 
                models.Q(away_team__slug=team)
            )  # <- this was missing
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = League.LEVEL_CHOICES
        context['sport_types'] = SportType.objects.all()
        return context

#results list
class ResultsListView(ListView):
    model = Match
    template_name = 'sports/results.html'
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        level = self.request.GET.get('level', None)
        sport_type = self.request.GET.get('sport_type', None)
        league = self.request.GET.get('league', None)
        team = self.request.GET.get('team', None)
        
        queryset = Match.objects.filter(status='finished').order_by('-match_date')
        
        if level:
            queryset = queryset.filter(league__level=level)
        if sport_type:
            queryset = queryset.filter(league__sport_type__slug=sport_type)
        if league:
            queryset = queryset.filter(league__slug=league)
        if team:
            queryset = queryset.filter(
                models.Q(home_team__slug=team) | 
                models.Q(away_team__slug=team))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = League.LEVEL_CHOICES
        context['sport_types'] = SportType.objects.all()
        return context


#news list
class NewsListView(ListView):
    model = News
    template_name = 'sports/news.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        sport_type = self.request.GET.get('sport_type', None)
        league = self.request.GET.get('league', None)
        team = self.request.GET.get('team', None)
        
        queryset = News.objects.all().order_by('-published_date')
        
        if sport_type:
            queryset = queryset.filter(related_sport__slug=sport_type)
        if league:
            queryset = queryset.filter(related_league__slug=league)
        if team:
            queryset = queryset.filter(related_team__slug=team)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sport_types'] = SportType.objects.all()
        return context


#news detail
class NewsDetailView(DetailView):
    model = News
    template_name = 'sports/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.object
        related_news = News.objects.filter(
            models.Q(related_sport=news.related_sport) |
            models.Q(related_league=news.related_league) |
            models.Q(related_team=news.related_team)
        ).exclude(id=news.id).order_by('-published_date')[:5]
        context['related_news'] = related_news
        return context