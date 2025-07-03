from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SportCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class SportType(models.Model):
    category = models.ForeignKey(SportCategory, related_name='sport_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class League(models.Model):
    LEVEL_CHOICES = [
        ('local', 'Local'),
        ('national', 'National'),
        ('international', 'International'),
    ]
    
    sport_type = models.ForeignKey(SportType, related_name='leagues', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    country = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='leagues/', blank=True, null=True)
    founded = models.PositiveIntegerField(blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.sport_type.name} - {self.name}"

class Team(models.Model):
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    short_name = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='teams/', blank=True, null=True)
    founded = models.PositiveIntegerField(blank=True, null=True)
    home_ground = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.league.name} - {self.name}"

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
        ('ALL', 'All-rounder'),
        # Add sport-specific positions as needed
    ]
    
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True)
    jersey_number = models.PositiveIntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # in meters
    weight = models.PositiveIntegerField(blank=True, null=True)  # in kg
    image = models.ImageField(upload_to='players/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team.name})"

class Match(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('postponed', 'Postponed'),
        ('canceled', 'Canceled'),
    ]
    
    league = models.ForeignKey(League, related_name='matches', on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    venue = models.CharField(max_length=100, blank=True)
    home_score = models.PositiveIntegerField(blank=True, null=True)
    away_score = models.PositiveIntegerField(blank=True, null=True)
    round = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "matches"
        ordering = ['match_date']

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} ({self.match_date})"

class MatchEvent(models.Model):
    EVENT_CHOICES = [
        ('goal', 'Goal'),
        ('assist', 'Assist'),
        ('yellow_card', 'Yellow Card'),
        ('red_card', 'Red Card'),
        ('sub_in', 'Substitution In'),
        ('sub_out', 'Substitution Out'),
        ('penalty', 'Penalty'),
        ('missed_penalty', 'Missed Penalty'),
        ('own_goal', 'Own Goal'),
        # Add sport-specific events as needed
    ]
    
    match = models.ForeignKey(Match, related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    player = models.ForeignKey(Player, related_name='events', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='events', on_delete=models.CASCADE)
    minute = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    additional_info = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.player} - {self.get_event_type_display()} ({self.minute}')"

class Standing(models.Model):
    league = models.ForeignKey(League, related_name='standings', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='standings', on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    played = models.PositiveIntegerField(default=0)
    won = models.PositiveIntegerField(default=0)
    drawn = models.PositiveIntegerField(default=0)
    lost = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    form = models.CharField(max_length=20, blank=True)  # Last 5 matches (W-W-D-L-W)

    class Meta:
        ordering = ['position']
        unique_together = ('league', 'team')

    def __str__(self):
        return f"{self.team.name} - {self.position} in {self.league.name}"

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_headline = models.BooleanField(default=False)
    related_sport = models.ForeignKey(SportType, related_name='news', on_delete=models.SET_NULL, blank=True, null=True)
    related_league = models.ForeignKey(League, related_name='news', on_delete=models.SET_NULL, blank=True, null=True)
    related_team = models.ForeignKey(Team, related_name='news', on_delete=models.SET_NULL, blank=True, null=True)
    related_player = models.ForeignKey(Player, related_name='news', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "news"
        ordering = ['-published_date']

    def __str__(self):
        return self.title