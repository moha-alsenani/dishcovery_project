from django import forms
from django.contrib.auth.models import User 
from dishcovery.models import UserProfile
from dishcovery.models import Recipe



class UserForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
     
     class Meta: 
         model = User
         fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('bio', 'picture',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'difficulty', 'cuisine', 'meal_type', 'diet', 'image']
