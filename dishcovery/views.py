from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from dishcovery.forms import UserForm, UserProfileForm, RecipeForm, CommentForm, RatingForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dishcovery.models import Recipe, Cuisine, Comment, Rating, User
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.utils.timezone import now

# Create your views here.

def home(request):
    trending_recipes = Recipe.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')[:4]  # Get top recipes by rating
    return render(request, 'dishcovery_project/home.html', {'trending_recipes': trending_recipes})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if user and user.is_active:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/dishcovery/'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid username or password.'})

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
            
            # Automatically log in the user after registration
            raw_password = user_form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            
            # Redirect to home page
            return redirect('dishcovery:home')
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

def search_view(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'dishcovery/search_results.html', {
        'query': query,
        'results': results
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            
            # Handle the cuisine - either find an existing one or create a new one
            cuisine_name = form.cleaned_data['cuisine_name']
            cuisine, created = Cuisine.objects.get_or_create(name=cuisine_name)
            recipe.cuisine = cuisine
            
            recipe.save()
            return redirect('dishcovery:profile_page')
    else:
        form = RecipeForm()

    return render(request, 'dishcovery_project/add_recipe.html', {'form': form})

# context processor function to make cuisines available to all templates
def cuisines_processor(request):
    cuisines = Cuisine.objects.all()
    return {'cuisines': cuisines}

@login_required
def profile_page(request):
    user_recipes = Recipe.objects.filter(author=request.user)
    show_edit_form = request.GET.get('edit_bio') == 'true'

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            
            # Handling the cuisine
            cuisine_name = form.cleaned_data['cuisine_name']
            cuisine, created = Cuisine.objects.get_or_create(name=cuisine_name)
            recipe.cuisine = cuisine
            
            recipe.save()
            return redirect('dishcovery:profile_page')
    else:
        form = RecipeForm()

    return render(request, 'dishcovery_project/profile_page.html', {
        'form': form, 
        'user_recipes': user_recipes,
        'show_edit_form': show_edit_form
    })

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and 'picture' in request.FILES:
        # Get the user's profile and update the picture
        profile = request.user.userprofile
        profile.picture = request.FILES['picture']
        profile.save()
    return redirect('dishcovery:profile_page')

@login_required
def update_bio(request):
    if request.method == 'POST':
        new_bio = request.POST.get('bio')
        if new_bio is not None:
            # Get the user's profile and update the bio
            profile = request.user.userprofile
            profile.bio = new_bio
            profile.save()
    return redirect('dishcovery:profile_page')

def other_user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    user_recipes = Recipe.objects.filter(author=profile_user)
    
    context = {
        'profile_user': profile_user,
        'user_recipes': user_recipes,
    }
    
    return render(request, 'dishcovery_project/other_user_profile.html', context)

def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = Comment.objects.filter(recipe=recipe).order_by('-created_at')
    average_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('score'))['score__avg']
    rating_form = RatingForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if 'rating' in request.POST:  # If rating form is submitted
            if request.user.is_authenticated:
                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    Rating.objects.filter(user=request.user, recipe=recipe).delete()
                    
                    Rating.objects.create(
                        user=request.user, recipe=recipe,
                        score=rating_form.cleaned_data['score']
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

# Commenting func with AJAX
def add_comment_ajax(request, recipe_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'You must be logged in to comment.'}, status=401)
    
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.created_at = now()
            comment.save()
            
            # Return the new comment data
            return JsonResponse({
                'status': 'success',
                'comment': {
                    'user': request.user.username,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime("%B %d, %Y %H:%M")
                }
            })
        else:
            return JsonResponse({'status': 'error', 'errors': comment_form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def cuisine_recipes(request, cuisine_id):
    cuisine = get_object_or_404(Cuisine, id=cuisine_id)  # Get the cuisine or return 404
    recipes = Recipe.objects.filter(cuisine=cuisine)  # Get recipes for the selected cuisine
    
    return render(request, 'dishcovery_project/cuisine_recipes.html', {'cuisine': cuisine, 'recipes': recipes})

def about(request):
    return render(request,'dishcovery_project/about.html')

def contact(request):
    return render(request,'dishcovery_project/contact.html')

def faq(request):
    return render(request,'dishcovery_project/faq.html' )


   
