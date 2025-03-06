from django.urls import path
from dishcovery import views

app_name = 'dishcovery'

urlpatterns = [
    path('', views.home, name='home'),
]