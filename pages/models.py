from django.db import models


class Feedback(models.Model):
    """Model for feedback"""

    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} feedback from {self.email}"
