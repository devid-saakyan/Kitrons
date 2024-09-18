from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class CustomUser(AbstractUser):
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.username

