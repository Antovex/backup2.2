# yourapp/models.py
from django.db import models
from django.contrib.auth.models import User
import secrets

class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, default=secrets.token_urlsafe(32))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Activation token for {self.user.username}"