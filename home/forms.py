from django import forms
from .models import Feedback, ContactMessage, Subscriber

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'feedback_text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'feedback_text': forms.Textarea(attrs={'placeholder': 'Your Feedback'}),
        }
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True) # Validates email format automatically.
    message = forms.CharField(widget=forms.Textarea, required=True) # Required message

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'email-input'
            })
        }