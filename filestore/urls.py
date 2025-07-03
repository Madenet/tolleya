from django.urls import path, include
from . import views

urlpatterns = [
    # Other URL patterns...
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('upload/', views.upload_file, name='upload_file'),
    path('add_to_cart/<int:file_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:file_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_uploaded_files/', views.view_uploaded_files, name='view_uploaded_files'),
    path('cart/', views.cart_view, name='cart_view'),
] 
