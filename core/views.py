from django.shortcuts import render
from django.views.generic import TemplateView
from questions.models import Question

class HomeView(TemplateView):
    """
    Home page view displaying the latest questions
    """
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the latest questions for the homepage
        context['questions'] = Question.objects.select_related('author').all()[:10]
        return context