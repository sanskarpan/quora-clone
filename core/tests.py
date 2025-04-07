from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from questions.models import Question

class HomeViewTest(TestCase):
    """
    Test case for the home page view
    """
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create some test questions
        for i in range(5):
            Question.objects.create(
                title=f'Test Question {i}',
                description=f'This is test question {i}',
                author=self.user
            )
            
    def test_home_view_get(self):
        """Test home page loads correctly"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        
    def test_home_view_context(self):
        """Test home page contains questions in context"""
        response = self.client.get(self.home_url)
        self.assertTrue('questions' in response.context)
        self.assertEqual(len(response.context['questions']), 5)
        
    def test_home_view_content(self):
        """Test home page shows questions"""
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Test Question 0')
        self.assertContains(response, 'Test Question 4')
        
    def test_home_view_authenticated(self):
        """Test home page with authenticated user"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ask a Question')
        self.assertContains(response, 'testuser')
        
    def test_home_view_unauthenticated(self):
        """Test home page with unauthenticated user"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')