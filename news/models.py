from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='ads/videos/', null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)