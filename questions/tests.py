from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm

class QuestionModelTest(TestCase):
    """
    Test case for Question model
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.question = Question.objects.create(
            title='Test Question',
            description='This is a test question',
            author=self.user
        )
        
    def test_question_creation(self):
        """Test question is created correctly"""
        self.assertEqual(self.question.title, 'Test Question')
        self.assertEqual(self.question.description, 'This is a test question')
        self.assertEqual(self.question.author, self.user)
        
    def test_question_str_method(self):
        """Test question string representation"""
        self.assertEqual(str(self.question), 'Test Question')
        
    def test_get_absolute_url(self):
        """Test get_absolute_url method"""
        expected_url = reverse('question-detail', kwargs={'pk': self.question.pk})
        self.assertEqual(self.question.get_absolute_url(), expected_url)
        
    def test_answer_count_property(self):
        """Test answer_count property returns correct count"""
        # Initially no answers
        self.assertEqual(self.question.answer_count, 0)
        
        # Add an answer
        Answer.objects.create(
            question=self.question,
            author=self.user,
            content='This is a test answer'
        )
        
        # Now should have 1 answer
        self.assertEqual(self.question.answer_count, 1)


class AnswerModelTest(TestCase):
    """
    Test case for Answer model
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.question = Question.objects.create(
            title='Test Question',
            description='This is a test question',
            author=self.user
        )
        self.answer = Answer.objects.create(
            question=self.question,
            author=self.user,
            content='This is a test answer'
        )
        
    def test_answer_creation(self):
        """Test answer is created correctly"""
        self.assertEqual(self.answer.question, self.question)
        self.assertEqual(self.answer.author, self.user)
        self.assertEqual(self.answer.content, 'This is a test answer')
        
    def test_answer_str_method(self):
        """Test answer string representation"""
        expected_str = f"Answer by {self.user.username} on '{self.question.title}'"
        self.assertEqual(str(self.answer), expected_str)
        
    def test_like_count_property(self):
        """Test like_count property returns correct count"""
        # Initially no likes
        self.assertEqual(self.answer.like_count, 0)
        
        # Add a like
        Like.objects.create(
            answer=self.answer,
            user=self.user
        )
        
        # Now should have 1 like
        self.assertEqual(self.answer.like_count, 1)


class LikeModelTest(TestCase):
    """
    Test case for Like model
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.question = Question.objects.create(
            title='Test Question',
            description='This is a test question',
            author=self.user
        )
        self.answer = Answer.objects.create(
            question=self.question,
            author=self.user,
            content='This is a test answer'
        )
        self.like = Like.objects.create(
            answer=self.answer,
            user=self.user
        )
        
    def test_like_creation(self):
        """Test like is created correctly"""
        self.assertEqual(self.like.answer, self.answer)
        self.assertEqual(self.like.user, self.user)
        
    def test_like_str_method(self):
        """Test like string representation"""
        expected_str = f"{self.user.username} likes answer by {self.user.username}"
        self.assertEqual(str(self.like), expected_str)
        
    def test_like_unique_constraint(self):
        """Test a user can only like an answer once"""
        # Trying to create duplicate like should raise IntegrityError
        with self.assertRaises(Exception):
            Like.objects.create(
                answer=self.answer,
                user=self.user
            )


class QuestionViewsTest(TestCase):
    """
    Test case for Question views
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.question = Question.objects.create(
            title='Test Question',
            description='This is a test question',
            author=self.user
        )
        self.question_list_url = reverse('question-list')
        self.question_detail_url = reverse('question-detail', kwargs={'pk': self.question.pk})
        self.question_create_url = reverse('question-create')
        self.question_update_url = reverse('question-update', kwargs={'pk': self.question.pk})
        self.question_delete_url = reverse('question-delete', kwargs={'pk': self.question.pk})
        
    def test_question_list_view(self):
        """Test question list view works correctly"""
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_list.html')
        self.assertContains(response, 'Test Question')
        
    def test_question_detail_view(self):
        """Test question detail view works correctly"""
        response = self.client.get(self.question_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_detail.html')
        self.assertContains(response, 'Test Question')
        self.assertContains(response, 'This is a test question')
        
    def test_question_create_view_authenticated(self):
        """Test authenticated user can access question create view"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.question_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_form.html')
        
    def test_question_create_view_unauthenticated(self):
        """Test unauthenticated user is redirected from question create view"""
        response = self.client.get(self.question_create_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.question_create_url}")
        
    def test_question_create_post(self):
        """Test creating a new question with post request"""
        self.client.login(username='testuser', password='testpassword123')
        question_data = {
            'title': 'New Test Question',
            'description': 'This is a new test question'
        }
        response = self.client.post(self.question_create_url, question_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Question.objects.filter(title='New Test Question').exists())
        
    def test_question_update_view_author(self):
        """Test question author can access update view"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.question_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_form.html')
        
    def test_question_update_view_not_author(self):
        """Test non-author cannot access question update view"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpassword123'
        )
        
        # Login as other user
        self.client.login(username='otheruser', password='testpassword123')
        
        # Try to access update page
        response = self.client.get(self.question_update_url)
        self.assertEqual(response.status_code, 403)  # Forbidden
        
    def test_question_delete_view_author(self):
        """Test question author can access delete view"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.question_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_confirm_delete.html')
        
    def test_question_delete_view_not_author(self):
        """Test non-author cannot access question delete view"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpassword123'
        )
        
        # Login as other user
        self.client.login(username='otheruser', password='testpassword123')
        
        # Try to access delete page
        response = self.client.get(self.question_delete_url)
        self.assertEqual(response.status_code, 403)  # Forbidden


class AnswerAndLikeViewsTest(TestCase):
    """
    Test case for Answer and Like views
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.question = Question.objects.create(
            title='Test Question',
            description='This is a test question',
            author=self.user
        )
        self.answer = Answer.objects.create(
            question=self.question,
            author=self.user,
            content='This is a test answer'
        )
        self.question_detail_url = reverse('question-detail', kwargs={'pk': self.question.pk})
        self.answer_update_url = reverse('answer-update', kwargs={'pk': self.answer.pk})
        self.answer_delete_url = reverse('answer-delete', kwargs={'pk': self.answer.pk})
        self.toggle_like_url = reverse('toggle-like', kwargs={'pk': self.answer.pk})
        
    def test_post_answer(self):
        """Test posting an answer to a question"""
        self.client.login(username='testuser', password='testpassword123')
        answer_data = {
            'content': 'This is another test answer'
        }
        response = self.client.post(self.question_detail_url, answer_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertRedirects(response, self.question_detail_url)
        self.assertEqual(Answer.objects.filter(question=self.question).count(), 2)
        
    def test_update_answer_author(self):
        """Test answer author can update their answer"""
        self.client.login(username='testuser', password='testpassword123')
        update_data = {
            'content': 'This is an updated test answer'
        }
        response = self.client.post(self.answer_update_url, update_data)
        self.assertEqual(response.status_code, 302)
        
        # Refresh answer from database
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.content, 'This is an updated test answer')
        
    def test_delete_answer_author(self):
        """Test answer author can delete their answer"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.answer_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.question_detail_url)
        self.assertEqual(Answer.objects.filter(id=self.answer.id).count(), 0)
        
    def test_toggle_like(self):
        """Test toggling like on an answer"""
        self.client.login(username='testuser', password='testpassword123')
        
        # Initially no likes
        self.assertEqual(Like.objects.filter(answer=self.answer, user=self.user).count(), 0)
        
        # Like the answer
        response = self.client.post(self.toggle_like_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Like.objects.filter(answer=self.answer, user=self.user).count(), 1)
        
        # Unlike the answer
        response = self.client.post(self.toggle_like_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Like.objects.filter(answer=self.answer, user=self.user).count(), 0)
        
    def test_toggle_like_ajax(self):
        """Test toggling like via AJAX"""
        self.client.login(username='testuser', password='testpassword123')
        
        # Like the answer
        response = self.client.post(
            self.toggle_like_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['liked'])
        self.assertEqual(response.json()['like_count'], 1)
        
        # Unlike the answer
        response = self.client.post(
            self.toggle_like_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['liked'])
        self.assertEqual(response.json()['like_count'], 0)


class FormTests(TestCase):
    """
    Test case for forms
    """
    def test_question_form_valid(self):
        """Test QuestionForm with valid data"""
        form_data = {
            'title': 'Test Question',
            'description': 'This is a test question'
        }
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_question_form_invalid(self):
        """Test QuestionForm with invalid data (empty title)"""
        form_data = {
            'title': '',
            'description': 'This is a test question'
        }
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        
    def test_answer_form_valid(self):
        """Test AnswerForm with valid data"""
        form_data = {
            'content': 'This is a test answer'
        }
        form = AnswerForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_answer_form_invalid(self):
        """Test AnswerForm with invalid data (empty content)"""
        form_data = {
            'content': ''
        }
        form = AnswerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)