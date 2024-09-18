from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    category = models.CharField(max_length=15)
    # Другие поля на основе схемы