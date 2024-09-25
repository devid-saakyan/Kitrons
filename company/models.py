from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(max_length=200)
    logo = models.ImageField()

    def __str__(self):
        return self.name