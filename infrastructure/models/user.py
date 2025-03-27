from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    documento = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return self.username
