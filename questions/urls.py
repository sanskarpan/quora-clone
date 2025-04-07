from django.urls import path
from . import views

urlpatterns = [
    # Question views
    path('', views.QuestionListView.as_view(), name='question-list'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('new/', views.QuestionCreateView.as_view(), name='question-create'),
    path('<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question-update'),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
    
    # Answer views
    path('answer/<int:pk>/update/', views.update_answer, name='answer-update'),
    path('answer/<int:pk>/delete/', views.delete_answer, name='answer-delete'),
    path('answer/<int:pk>/like/', views.toggle_like, name='toggle-like'),
]