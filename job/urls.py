from django.urls import path
from . import views
from django.views.generic import ListView
from .views import jobgalleryview, addJob, jobgallery, viewJob, deleteJob, JobCategoryView

#GalleryView
urlpatterns = [ 
    path('', views.jobgallery, name='jobgallery'),
    path('job/<str:pk>/', views.viewJob, name='job'),
    path('add/', views.addJob, name='add'),
    #job list
    path('joblistview/', views.jobgalleryview, name='joblistview'),
    path('applicationview/', views.applicationview, name='applicationview'),
    path('apply/', views.applyJob, name='apply'),
    #end
    path('delete-job/<str:pk>', views.deleteJob, name="delete-job"),
    path('category/<str:cats>/', views.JobCategoryView, name='category'),
]
