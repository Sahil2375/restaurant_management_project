from django.db import models

# Create your models here.

class Feedback(models.Model):
    "Stores customer feedback"
    comments = models.TextField(help_text="Customer feedback comments.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"