from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    """
    Form for creating and updating questions
    """
    class Meta:
        model = Question
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def clean_title(self):
        """
        Validate that the title is not empty or just whitespace
        """
        title = self.cleaned_data.get('title')
        if not title or title.isspace():
            raise forms.ValidationError('Title cannot be empty.')
        return title


class AnswerForm(forms.ModelForm):
    """
    Form for creating and updating answers
    """
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your answer here...'}),
        }
        labels = {
            'content': '',
        }
    
    def clean_content(self):
        """
        Validate that the content is not empty or just whitespace
        """
        content = self.cleaned_data.get('content')
        if not content or content.isspace():
            raise forms.ValidationError('Answer cannot be empty.')
        return content