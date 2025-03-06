from django.contrib import admin
from .models import UserProfile, Cuisine, Recipe, Comment, Rating

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Cuisine)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Rating)