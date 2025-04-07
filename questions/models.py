from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Question(models.Model):
    """
    Model representing a user's question
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})
    
    @property
    def answer_count(self):
        return self.answers.count()


class Answer(models.Model):
    """
    Model representing an answer to a question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['question']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"Answer by {self.author.username} on '{self.question.title}'"
    
    @property
    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    """
    Model representing a user liking an answer
    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        # Ensure a user can only like an answer once
        unique_together = ('answer', 'user')
        indexes = [
            models.Index(fields=['answer']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes answer by {self.answer.author.username}"