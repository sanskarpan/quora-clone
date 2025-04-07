from django.contrib import admin
from .models import Question, Answer, Like

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model
    """
    list_display = ('title', 'author', 'created_at', 'updated_at', 'answer_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def answer_count(self, obj):
        """
        Count answers for this question
        """
        return obj.answers.count()
    answer_count.short_description = 'Answers'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Answer model
    """
    list_display = ('question_title', 'author', 'created_at', 'updated_at', 'like_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'question__title')
    readonly_fields = ('created_at', 'updated_at')
    
    def question_title(self, obj):
        """
        Get the title of the related question
        """
        return obj.question.title
    question_title.short_description = 'Question'
    
    def like_count(self, obj):
        """
        Count likes for this answer
        """
        return obj.likes.count()
    like_count.short_description = 'Likes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Like model
    """
    list_display = ('user', 'answer_author', 'question_title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'answer__author__username', 'answer__question__title')
    readonly_fields = ('created_at',)
    
    def answer_author(self, obj):
        """
        Get the author of the related answer
        """
        return obj.answer.author.username
    answer_author.short_description = 'Answer Author'
    
    def question_title(self, obj):
        """
        Get the title of the related question
        """
        return obj.answer.question.title
    question_title.short_description = 'Question'