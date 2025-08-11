from django import forms
from .models import Feedback, ContactMessage

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

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'})
        }