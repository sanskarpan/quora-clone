from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm

class UserRegistrationTest(TestCase):
    """
    Test case for user registration functionality
    """
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        
    def test_registration_view_get(self):
        """Test registration page loads correctly"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)
        
    def test_registration_valid_post(self):
        """Test user registration with valid data"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
    # def test_registration_invalid_post(self):
    #     """Test user registration with invalid data (password mismatch)"""
    #     invalid_data = self.user_data.copy()
    #     invalid_data['password2'] = 'wrongpassword'
    #     response = self.client.post(self.register_url, invalid_data)
    #     self.assertEqual(response.status_code, 200)  # Stay on the same page
    #     self.assertFalse(User.objects.filter(username='testuser').exists())

    #     # Get the form from the context
    #     form = response.context['form']
    #     self.assertTrue(form.errors)
    #     self.assertIn('password2', form.errors)
    #     error_message = form.errors['password2'][0]
    #     self.assertTrue("password fields didn't match" in error_message)

class UserProfileTest(TestCase):
    """
    Test case for user profile functionality
    """
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
    def test_profile_view_authenticated(self):
        """Test profile page loads for authenticated user"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        
    def test_profile_view_unauthenticated(self):
        """Test profile page redirects for unauthenticated user"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.profile_url}")
        
    def test_profile_update(self):
        """Test profile update with valid data"""
        self.client.login(username='testuser', password='testpassword123')
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'This is a test bio'
        }
        response = self.client.post(self.profile_url, update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.bio, 'This is a test bio')

class ProfileModelTest(TestCase):
    """
    Test case for Profile model
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
    def test_profile_creation(self):
        """Test profile is automatically created for new user"""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        
    def test_profile_str_method(self):
        """Test profile string representation"""
        profile = self.user.profile
        self.assertEqual(str(profile), "testuser's Profile")

class LogoutTest(TestCase):
    """
    Test case for logout functionality
    """
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
    def test_logout_view(self):
        """Test logout view works correctly"""
        # First login
        self.client.login(username='testuser', password='testpassword123')
        
        # Verify user is logged in
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Should access profile when logged in
        
        # Logout
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('home'))
        
        # Verify user is logged out
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

