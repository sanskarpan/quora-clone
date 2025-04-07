from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm

class QuestionListView(ListView):
    """
    View for listing all questions with pagination
    """
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Get all questions with prefetched author and answer count
        """
        return Question.objects.select_related('author').prefetch_related('answers').all()


class QuestionDetailView(DetailView):
    """
    View for displaying question details with answers
    """
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add form for submitting a new answer
        context['answer_form'] = AnswerForm()
        
        # Get answers with prefetched authors and likes
        answers = self.object.answers.select_related('author').prefetch_related('likes').all()
        
        # Add user's likes to context if user is authenticated
        if self.request.user.is_authenticated:
            user_likes = set(Like.objects.filter(
                user=self.request.user, 
                answer__in=answers
            ).values_list('answer_id', flat=True))
            
            context['user_likes'] = user_likes
        
        context['answers'] = answers
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to add a new answer
        """
        if not request.user.is_authenticated:
            return redirect('login')
            
        question = self.get_object()
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            messages.success(request, 'Your answer has been added successfully!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
        
        return redirect('question-detail', pk=question.pk)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new question
    """
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    
    def form_valid(self, form):
        """
        Set the author to the current user before saving
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your question has been created successfully!')
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing question
    """
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    
    def form_valid(self, form):
        """
        Set the author to the current user before saving
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your question has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Check if the current user is the author of the question
        """
        question = self.get_object()
        return self.request.user == question.author


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a question
    """
    model = Question
    template_name = 'questions/question_confirm_delete.html'
    success_url = reverse_lazy('question-list')
    
    def delete(self, request, *args, **kwargs):
        """
        Show success message after deletion
        """
        messages.success(self.request, 'Your question has been deleted.')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """
        Check if the current user is the author of the question
        """
        question = self.get_object()
        return self.request.user == question.author


@login_required
def update_answer(request, pk):
    """
    View for updating an answer
    """
    answer = get_object_or_404(Answer, pk=pk)
    
    # Check if the user is the author
    if request.user != answer.author:
        messages.error(request, "You cannot edit someone else's answer.")
        return redirect('question-detail', pk=answer.question.pk)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your answer has been updated successfully!')
            return redirect('question-detail', pk=answer.question.pk)
    else:
        form = AnswerForm(instance=answer)
    
    return render(request, 'questions/answer_form.html', {
        'form': form,
        'answer': answer
    })


@login_required
def delete_answer(request, pk):
    """
    View for deleting an answer
    """
    answer = get_object_or_404(Answer, pk=pk)
    question_pk = answer.question.pk
    
    # Check if the user is the author
    if request.user != answer.author:
        messages.error(request, "You cannot delete someone else's answer.")
    else:
        answer.delete()
        messages.success(request, 'Your answer has been deleted successfully!')
    
    return redirect('question-detail', pk=question_pk)


@login_required
def toggle_like(request, pk):
    """
    View for toggling like on an answer
    AJAX-compatible endpoint for liking/unliking
    """
    answer = get_object_or_404(Answer, pk=pk)
    user = request.user
    
    # Check if the user already liked this answer
    like_exists = Like.objects.filter(answer=answer, user=user).exists()
    
    if like_exists:
        # Unlike
        Like.objects.filter(answer=answer, user=user).delete()
        liked = False
    else:
        # Like
        Like.objects.create(answer=answer, user=user)
        liked = True
    
    # Return JSON response for AJAX or redirect for non-AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'like_count': answer.like_count
        })
    else:
        return redirect('question-detail', pk=answer.question.pk)