from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comments']
        widgets = {
            'comments' : forms.Textarea(attrs={
                'rows' : 4,
                'placeholder' : 'Write your feedback here...',
                'class' : 'feedback-textarea'
            })
        }
        labels = {
            'comments' : 'Your Feedback'
        }