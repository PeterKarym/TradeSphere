from django.db import models

class EmailVerification(models.Model):
    email = models.EmailField()
    verification_code = models.CharField(max_length=10)  # Adjust the max_length as needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.verification_code}"
