from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid


class CustomUser(AbstractUser):
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    groups = models.ManyToManyField(Group,
                                    blank=True,
                                    related_name='customuser_set')

    user_permissions = models.ManyToManyField(Permission,
                                              related_name='customuser_set',
                                              blank=True,)

    def __str__(self):
        return self.username

