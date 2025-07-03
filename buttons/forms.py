from django import forms
from .models import TermsOfUse, PrivacyPolicy

#terms of use and privacy policy
class TermsOfUseForm(forms.ModelForm):
    class Meta:
        model = TermsOfUse
        fields = ['title', 'content']

class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['title', 'content']