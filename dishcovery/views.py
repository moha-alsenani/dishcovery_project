from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from dishcovery.forms import UserForm, UserProfileForm, RecipeForm, CommentForm, RatingForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dishcovery.models import Recipe, Cuisine, Comment, Rating
from django.db.models import Avg

# Create your views here.

def home(request):
    cuisines = Cuisine.objects.all()
    return render(request, 'dishcovery_project/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('dishcovery:home'))
            else:
                return HttpResponse("Your Dishcovery account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'dishcovery_project/login.html')
    
def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'dishcovery_project/register.html', {
    'user_form': user_form,
    'profile_form': profile_form,
    'registered': registered
})

@login_required
def profile_page(request):
    user_recipes = Recipe.objects.filter(author=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  
            recipe.save()
            return redirect('dishcovery:profile_page')  
    else:
        form = RecipeForm()

    return render(request, 'dishcovery_project/profile_page.html', {'form': form, 'user_recipes': user_recipes})

def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all().order_by('-created_at')  # Fetch all comments
    average_rating = recipe.ratings.aggregate(Avg('score'))['score__avg']  # Calculate average rating
    rating_form = RatingForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if 'rating' in request.POST:  # If rating form is submitted
            if request.user.is_authenticated:
                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    rating, created = Rating.objects.update_or_create(
                        user=request.user, recipe=recipe,
                        defaults={'score': rating_form.cleaned_data['score']}
                    )
                    return redirect('dishcovery:recipe_details', recipe_id=recipe.id)
            else:
                return HttpResponse("You must be logged in to rate.")

        elif 'comment' in request.POST:  # If comment form is submitted
            if request.user.is_authenticated:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.recipe = recipe
                    comment.user = request.user
                    comment.save()
                    return redirect('dishcovery:recipe_details', recipe_id=recipe.id)
            else:
                return HttpResponse("You must be logged in to comment.")

    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': round(average_rating, 1) if average_rating else "No ratings yet"
    }
    return render(request, 'dishcovery_project/recipe_details.html', context)



def cuisine_recipes(request, cuisine_id):
    cuisine = get_object_or_404(Cuisine, id=cuisine_id)  # Get the cuisine or return 404
    recipes = Recipe.objects.filter(cuisine=cuisine)  # Get recipes for the selected cuisine
    
    return render(request, 'dishcovery_project/cuisine_recipes.html', {'cuisine': cuisine, 'recipes': recipes})






   
