from django.conf import settings
from django.db import models
from django.utils import timezone


class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    last_withdraw = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.available_balance}"


class BalanceActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[('video', 'Video'), ('post', 'Post'), ('survey', 'Survey')])
    date = models.DateField()
    views = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.date}"


class Withdraw(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdraw_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.withdraw_date}"

