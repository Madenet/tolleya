from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, date 
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
#qrcode 
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
#create your models here
NEWS = "News"
EVENTS = "Event"

POST = (
    (NEWS, "News"),
    (EVENTS, "Event"),
)



#news portal

# QuerySet for NewsAndEvents
class NewsAndEventsQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(summary__icontains=query) | Q(posted_as__icontains=query)
        return self.filter(lookups).distinct()

# Manager for NewsAndEvents
class NewsAndEventsManager(models.Manager):
    def get_queryset(self):
        return NewsAndEventsQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

# NewsAndEvents model
class NewsAndEvents(models.Model):
    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=2000, blank=True, null=True)
    posted_as = models.CharField(choices=POST, max_length=10)
    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="news_images/%y/%m/%d/", default="default.png", null=True)
    objects = NewsAndEventsManager()

    # Get the image URL or the default image
    def get_image(self):
        try:
            return self.image.url
        except:
            return settings.MEDIA_URL + "default.png"

    # Resize the image if necessary
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except:
            pass

    # Delete the image file if it's not the default image
    def delete(self, *args, **kwargs):
        if self.image.url != settings.MEDIA_URL + "default.png":
            self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
#End

#open profile page and web link.
class UserProfile(models.Model): #user will be accessed at their businesses and websites
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField()
    picture = models.ImageField(null=True, blank=True, upload_to="images/profile/", default='profile_img/925667.jpg')
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    #This is my whatsapp field to edit my whatsapp account as a record and comment section
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    #End
    website_url = models.CharField(max_length=200, null=True, blank=True)
    google_url = models.CharField(max_length=200, null=True, blank=True)
    zoom_url = models.CharField(max_length=200, null=True, blank=True)
    microsoftTeam_url = models.CharField(max_length=200, null=True, blank=True)
    playstore_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=100,null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    telegram_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    thread_url = models.CharField(max_length=200, null=True, blank=True)
    youtube_url = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    pinterest_url = models.CharField(max_length=200, null=True, blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    qr_name  = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    #qr_code
    def __str__(self):
        return str(self.qr_name)
    
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.qr_name)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        fqr_name = f'qr_code-{self.qr_name}.png'
        buffer = BytesIO()
        qrcode_img.save(buffer, 'PNG')
        self.qr_code.save(fqr_name, File(buffer), save=False)
        buffer.close()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()   


def __str__(self):
    return str(self.user)


    def get_absolute_url(self):
        return reverse('home', kwargs={'pk': self.pk})

#colors post form
class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/", )
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    #body = RichTextField(blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    #colors caroursel slide post images
    image = models.ImageField(upload_to="carousel/%y/%m/%d/" ,blank=True, null=True,  default='/static/img/default-user.png')
    title = models.CharField(max_length=150)
    tags = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.CharField(max_length=100)
 
    #corousel views
    def __Str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def __str__(self): 
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        #return reverse("article-detail", args=(str(self.id)) )
        return reverse('home')


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    def children(self): 
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

 	
#add notification app here
class Notification(models.Model):
    # 1 = like, 2= Comment,
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)


class PostActivity(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=[('win', 'Win'), ('loss', 'Loss')])
    details = models.TextField()
    strategy = models.TextField(blank=True, null=True)
    analysis = models.TextField(blank=True, null=True)
    improvement = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.post.title} Activity'

#trade activity model:
class TradingActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

   