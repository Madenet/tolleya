from django.contrib import admin
from .models import TermsOfUse, PrivacyPolicy
# Register your models here.
admin.site.register(TermsOfUse)
admin.site.register(PrivacyPolicy)