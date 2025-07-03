from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#files
class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=False, blank=False)
    zipped_file = models.FileField(upload_to='zipped_files/')
    zoom_url = models.CharField(max_length=200, null=True, blank=True)
    microsoftTeam_url = models.CharField(max_length=200, null=True, blank=True)
    gmail_url = models.CharField(max_length=200, null=True, blank=True)
    website_url = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    playstore_url = models.CharField(max_length=200, null=True, blank=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    pinterest_url = models.CharField(max_length=200, null=True, blank=True)
    youtube_url = models.CharField(max_length=200, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
   
    def __str__(self):
        return self.description
    # Other fields...

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

#models to view the liked files 

class FileLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
   


