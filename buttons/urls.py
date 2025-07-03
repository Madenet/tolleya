from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_button, name='add_button'),
    path('view/', views.view_buttons, name='view_buttons'),
    path('remove/<int:button_id>/', views.remove_button, name='remove_button'),
    path('shared/<uuid:share_id>/', views.shared_button, name='shared_button'),
    #terms of use
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

]
