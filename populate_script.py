import os
import django

# Set up Django environment (Replace 'your_project' with your actual project name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dishcovery_project.settings')

# Initialize Django
django.setup()

# Now import models
from django.contrib.auth.models import User
from dishcovery.models import UserProfile, Cuisine, Recipe, Comment, Rating

# Sample data
def populate():
    # Create Cuisines
    cuisines = ["Italian", "Mexican", "Indian", "Chinese", "French", "Japanese", "Thai"]
    for name in cuisines:
        Cuisine.objects.get_or_create(name=name)

    # Create Users and Profiles
    users_data = [
        {"username": "moha_als", "email": "Moha@example.com", "password": "test123"},
        {"username": "otis", "email": "Otis@example.com", "password": "test123"},
    ]
    
    users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(username=user_data["username"], email=user_data["email"])
        if created:
            user.set_password(user_data["password"])
            user.save()
            UserProfile.objects.get_or_create(user=user)
        users[user_data["username"]] = user

    # Create Recipes
    recipes_data = [
        {"title": "Pasta Carbonara", "author": "moha_als", "ingredients": "Pasta, Eggs, Bacon, Cheese", "instructions": "Boil pasta...", "cuisine": "Italian", "difficulty": "Easy", "meal_type": "Dinner"},
        {"title": "Sushi Rolls", "author": "otis", "ingredients": "Rice, Nori, Fish", "instructions": "Roll sushi...", "cuisine": "Japanese", "difficulty": "Medium", "meal_type": "Lunch"},
    ]
    
    recipes = []
    for recipe_data in recipes_data:
        user = users[recipe_data["author"]]
        cuisine = Cuisine.objects.get(name=recipe_data["cuisine"])
        recipe = Recipe.objects.create(
            title=recipe_data["title"],
            author=user,
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            cuisine=cuisine,
            difficulty=recipe_data["difficulty"],
            meal_type=recipe_data["meal_type"],
        )
        recipes.append(recipe)

    # Create Comments
    Comment.objects.create(user=users["moha_als"], recipe=recipes[0], text="Looks delicious!")
    Comment.objects.create(user=users["otis"], recipe=recipes[1], text="Can't wait to try this!")

    # Create Ratings
    Rating.objects.create(user=users["moha_als"], recipe=recipes[0], score=5)
    Rating.objects.create(user=users["otis"], recipe=recipes[1], score=4)

    print("✅ Database populated successfully!")

if __name__ == "__main__":
    populate()
