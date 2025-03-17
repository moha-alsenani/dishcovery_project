from django.urls import path
from dishcovery import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from dishcovery_project import settings

app_name = 'dishcovery'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dishcovery:home'), name='logout'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('recipe/<int:recipe_id>/', views.recipe_details, name='recipe_details'),
    path('cuisine/<int:cuisine_id>/', views.cuisine_recipes, name='cuisine_recipes'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)