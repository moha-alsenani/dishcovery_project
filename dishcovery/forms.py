from django import forms
from django.contrib.auth.models import User 
from dishcovery.models import UserProfile, Recipe, Comment, Rating



class UserForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
     
     class Meta: 
         model = User
         fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('bio', 'picture',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'difficulty', 'cuisine', 'meal_type', 'diet', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'form-control'}),
        }
