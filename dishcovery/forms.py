from django import forms
from django.contrib.auth.models import User 
from dishcovery.models import UserProfile, Recipe, Comment, Rating


# user form (registering)
class UserForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
     
     class Meta: 
         model = User
         fields = ('username', 'email', 'password')

#Profile page form
class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('bio', 'picture',)

#recipe / adding recipe form
class RecipeForm(forms.ModelForm):
    cuisine_name = forms.CharField(max_length=100, required=True, help_text="Enter the cuisine...")
    
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'difficulty', 'meal_type', 'diet', 'image']        

# Commenting
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }

# Rating
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'form-control'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)