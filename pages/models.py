from django.db import models


class Feedback(models.Model):
    """Model for feedback"""

    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.subject} feedback from {self.email}"
