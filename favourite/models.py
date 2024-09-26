from django.db import models
from django.conf import settings


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey('ads.BaseAd', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'ad')  # Уникальность: один пользователь может добавлять одну рекламу только один раз

    def __str__(self):
        return f"{self.user.username} - {self.ad.title}"
