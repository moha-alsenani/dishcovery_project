from django.test import TestCase, Client
from django.contrib.auth.models import User
from dishcovery.models import UserProfile, Cuisine, Recipe, Comment, Rating
from django.db.models import Avg
from django.urls import reverse

# Create your tests here.

# Testing Models
class ModelTests(TestCase):

    def setUp(self):
        """Set up test data for models"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.recipe = Recipe.objects.create(
            title="Pasta Carbonara",
            author=self.user,
            ingredients="Pasta, Eggs, Cheese, Bacon",
            instructions="Boil pasta, mix with eggs and cheese, add bacon.",
            difficulty="Medium",
            cuisine=self.cuisine,
            meal_type="Dinner",
            diet="None"
        )

    def test_user_profile_creation(self):
        """Test that a UserProfile is created properly"""
        profile = UserProfile.objects.create(user=self.user, bio="Love cooking!")
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.bio, "Love cooking!")

    def test_cuisine_creation(self):
        """Test that a Cuisine is created properly"""
        cuisine = Cuisine.objects.create(name="Mexican")
        self.assertEqual(str(cuisine), "Mexican")

    def test_recipe_creation(self):
        """Test that a Recipe is created properly"""
        self.assertEqual(str(self.recipe), "Pasta Carbonara")
        self.assertEqual(self.recipe.author.username, "testuser")
        self.assertEqual(self.recipe.cuisine.name, "Italian")

    def test_comment_creation(self):
        """Test that a Comment is created properly"""
        comment = Comment.objects.create(user=self.user, recipe=self.recipe, text="Looks delicious!")
        self.assertEqual(str(comment), "testuser on Pasta Carbonara")
        self.assertEqual(comment.recipe.title, "Pasta Carbonara")
        self.assertEqual(comment.user.username, "testuser")

    def test_rating_creation(self):
        """Test that a Rating is created properly"""
        rating = Rating.objects.create(user=self.user, recipe=self.recipe, score=9)
        self.assertEqual(str(rating), "9/10 by testuser")
        self.assertEqual(rating.recipe.title, "Pasta Carbonara")
        self.assertEqual(rating.score, 9)

    def test_average_rating(self):
        """Test that average rating calculation works"""
        Rating.objects.create(user=self.user, recipe=self.recipe, score=8)
        Rating.objects.create(user=self.user, recipe=self.recipe, score=10)

        avg_rating = self.recipe.ratings.aggregate(Avg('score'))['score__avg']
        self.assertAlmostEqual(avg_rating, 9.0, places=1)  # Should be (8+10)/2 = 9.0


# Testing the views (not all views are included)

class ViewTests(TestCase):

    def setUp(self):
        """Set up test data for views"""
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='password_123')
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.recipe = Recipe.objects.create(
            title="Pasta Carbonara",
            author=self.user,
            ingredients="Pasta, Eggs, Cheese, Bacon",
            instructions="Boil pasta, mix with eggs and cheese, add Haggis.",
            difficulty="Medium",
            cuisine=self.cuisine,
            meal_type="Dinner",
            diet="None"
        )

    def test_home_view(self):
        """Test home page loads successfully with trending recipes"""
        response = self.client.get(reverse('dishcovery:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/home.html')

    def test_user_login_view_valid(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('dishcovery:login'), {'username': 'test_user', 'password': 'password_123'})
        self.assertEqual(response.status_code, 200)  # Should redirect after login

    def test_register_view(self):
        """Test user registration"""
        response = self.client.post(reverse('dishcovery:home'), {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'test_pass123'
        })
        self.assertEqual(response.status_code, 200)  # Should return the registration page

    def test_profile_page_view_authenticated(self):
        """Test profile page for logged-in user"""
        self.client.login(username='test_user', password='password_123')
        response = self.client.get(reverse('dishcovery:profile_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/profile_page.html')

    def test_profile_page_view_unauthenticated(self):
        """Test profile page redirects unauthenticated users"""
        response = self.client.get(reverse('dishcovery:profile_page'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_recipe_details_view(self):
        """Test recipe details page loads"""
        response = self.client.get(reverse('dishcovery:recipe_details', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/recipe_details.html')

    def test_add_comment_authenticated(self):
        """Test authenticated user can add a comment"""
        self.client.login(username='test_user', password='password_123')
        response = self.client.post(reverse('dishcovery:recipe_details', args=[self.recipe.id]), {'text': 'Great recipe!', 'comment': True})
        self.assertEqual(response.status_code, 302)  # Should redirect after posting

        comment_exists = Comment.objects.filter(recipe=self.recipe, text="Great recipe!").exists()
        self.assertTrue(comment_exists)

    def test_add_comment_unauthenticated(self):
        """Test unauthenticated users cannot comment"""
        response = self.client.post(reverse('dishcovery:recipe_details', args=[self.recipe.id]), {'text': 'Great recipe!', 'comment': True})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must be logged in to comment.")

    def test_add_rating_authenticated(self):
        """Test authenticated user can add a rating"""
        self.client.login(username='test_user', password='password_123')
        response = self.client.post(reverse('dishcovery:recipe_details', args=[self.recipe.id]), {'score': 9, 'rating': True})
        self.assertEqual(response.status_code, 302)  # Should redirect after posting

        rating_exists = Rating.objects.filter(recipe=self.recipe, score=9).exists()
        self.assertTrue(rating_exists)

    def test_add_rating_unauthenticated(self):
        """Test unauthenticated users cannot rate"""
        response = self.client.post(reverse('dishcovery:recipe_details', args=[self.recipe.id]), {'score': 9, 'rating': True})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must be logged in to rate.")

    def test_cuisine_recipes_view(self):
        """Test cuisine-specific recipes page loads"""
        response = self.client.get(reverse('dishcovery:cuisine_recipes', args=[self.cuisine.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/cuisine_recipes.html')

    def test_about_view(self):
        """Test about page loads successfully"""
        response = self.client.get(reverse('dishcovery:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/about.html')

    def test_contact_view(self):
        """Test contact page loads successfully"""
        response = self.client.get(reverse('dishcovery:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/contact.html')

    def test_faq_view(self):
        """Test FAQ page loads successfully"""
        response = self.client.get(reverse('dishcovery:faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/faq.html')

    def test_add_recipe_authenticated(self):
        """Test authenticated user can access add recipe page"""
        self.client.login(username='test_user', password='password_123')
        response = self.client.get(reverse('dishcovery:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/add_recipe.html')

    def test_add_recipe_unauthenticated(self):
        """Test unauthenticated user is redirected from add recipe page"""
        response = self.client.get(reverse('dishcovery:add_recipe'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_add_recipe_post(self):
        """Test adding a new recipe"""
        self.client.login(username='test_user', password='password_123')
        recipe_data = {
            'title': 'Test Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'difficulty': 'Easy',
            'cuisine_name': self.cuisine.id,
            'meal_type': 'Breakfast',
            'diet': 'Vegetarian'
        }
        response = self.client.post(reverse('dishcovery:profile_page'), recipe_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after posting
        
        # Check if recipe was created
        recipe_exists = Recipe.objects.filter(title='Test Recipe').exists()
        self.assertTrue(recipe_exists)

    def test_other_user_profile_view(self):
        """Test viewing another user's profile"""
        response = self.client.get(reverse('dishcovery:other_user_profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishcovery_project/other_user_profile.html')

    def test_add_comment_ajax(self):
        """Test adding a comment via AJAX"""
        self.client.login(username='test_user', password='password_123')
        response = self.client.post(
            reverse('dishcovery:add_comment_ajax', args=[self.recipe.id]),
            {'text': 'Ajax comment test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Check if comment was created
        comment_exists = Comment.objects.filter(recipe=self.recipe, text='Ajax comment test').exists()
        self.assertTrue(comment_exists)

    def test_add_comment_ajax_unauthenticated(self):
        """Test adding a comment via AJAX while unauthenticated"""
        response = self.client.post(
            reverse('dishcovery:add_comment_ajax', args=[self.recipe.id]),
            {'text': 'Unauthenticated comment'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertEqual(response.json()['status'], 'error')

    def test_user_login_ajax(self):
        """Test login with AJAX request"""
        response = self.client.post(
            reverse('dishcovery:login'),
            {'username': 'test_user', 'password': 'password_123'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_user_login_ajax_invalid(self):
        """Test login with invalid credentials using AJAX"""
        response = self.client.post(
            reverse('dishcovery:login'),
            {'username': 'wrong_user', 'password': 'wrong_password'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_register_post_success(self):
        """Test successful user registration"""
        user_data = {
            'username': 'new_test_user',
            'email': 'new_test@example.com',
            'password': 'new_password123',
        }
        profile_data = {
            'bio': 'Test bio',
        }
        # Combine the dictionaries
        form_data = {**user_data, **profile_data}
        
        response = self.client.post(reverse('dishcovery:register'), form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect to home after successful registration
        
        # Check if user was created
        user_exists = User.objects.filter(username='new_test_user').exists()
        self.assertTrue(user_exists)