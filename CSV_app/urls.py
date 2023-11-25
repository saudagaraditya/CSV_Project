
from django.urls import path
from .views import upload_file, display_users, download_csv

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('display/', display_users, name='display_users'),
    path('download_csv/', download_csv, name='download_csv'),
    
]
