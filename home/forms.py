from django import forms
from .models import Feedback, ContactMessage

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

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Your message must be at least 10 characters long.")
        return message