from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomButton, TermsOfUse, PrivacyPolicy

#add buttons
@login_required
def add_button(request):
    if request.method == 'POST':
        # Get the data from the request
        logo = request.FILES.get('logo')
        web_url = request.POST.get('web_url')
        
        # Check if required fields are provided
        if not logo or not web_url:
            return HttpResponse('Please provide both logo and web URL.', status=400)
        
        # Create a CustomButton instance
        button = CustomButton(
            logo=logo,
            web_url=web_url,
            user=request.user
        )

        try:
            button.save()
            return redirect('home')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}', status=500)

    # Handle GET request (initial form display)
    return render(request, 'buttons/add_button.html')


@login_required
def view_buttons(request):
    buttons = CustomButton.objects.filter(user=request.user)
    return render(request, 'buttons/view_buttons.html', {'buttons': buttons})

@login_required
def remove_button(request, button_id):
    button = CustomButton.objects.get(pk=button_id)
    if request.user == button.user:
        button.delete()
    return redirect('view_buttons')

#share button
def shared_button(request, share_id):
    button = get_object_or_404(CustomButton, share_id=share_id)
    return render(request, 'buttons/shared_button.html', {'button': button})

#terms of use and privacy policy
def terms_of_use(request):
    terms = TermsOfUse.objects.latest('last_updated')
    return render(request, 'terms_of_use.html', {'terms': terms})

def privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.latest('last_updated')
    return render(request, 'privacy_policy.html', {'privacy_policy': privacy_policy})