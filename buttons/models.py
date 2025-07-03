from django.db import models
import uuid
# Create your models here.

class CustomButton(models.Model):
    logo = models.ImageField(upload_to='buttons/')
    web_url = models.URLField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.web_url

#models for privacy and terms of use
class TermsOfUse(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)