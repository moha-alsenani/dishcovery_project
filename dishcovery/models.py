from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    
class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)  
    meal_type = models.CharField(max_length=50, choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Dessert', 'Dessert')])
    diet = models.CharField(max_length=50, blank=True, null=True, choices=[('Vegan', 'Vegan'), ('Keto', 'Keto'), ('Vegetarian', 'Vegetarian'), ('None', 'None')])
    image = models.ImageField(upload_to='recipe_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the comment
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')  # Recipe being commented on
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.recipe.title}"


    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)])  # Updated to 1-10 scale

    def __str__(self):
        return f"{self.score}/10 by {self.user.username}"



