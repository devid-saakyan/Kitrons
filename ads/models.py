from django.db import models
from django.conf import settings


class BaseAd(models.Model):
    AD_TYPES = [
        ('survey', 'Surveys'),
        ('video', 'Videos'),
        ('post', 'Posts'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    ad_type = models.CharField(max_length=10, choices=AD_TYPES)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    category = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_boosted = models.BooleanField(default=False)
    boost_end_date = models.DateTimeField(null=True, blank=True)

    post_text = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to='ads/videos/', null=True, blank=True)

    @property
    def boost(self):
        return {
            'isBoost': self.is_boosted,
            'multiplier': 1,
            'boostEndDate': self.boost_end_date,
        }

    def __str__(self):
        return self.title


class AdImage(models.Model):
    ad = models.ForeignKey('BaseAd', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads/images/')
    created_at = models.DateTimeField(auto_now_add=True)


class AdQuestion(models.Model):
    ad = models.ForeignKey('BaseAd', on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    correct_answer = models.ForeignKey('AdAnswer', null=True, blank=True, on_delete=models.CASCADE, related_name='correct_answer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text


class AdAnswer(models.Model):
    question = models.ForeignKey('AdQuestion', on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text


class UserAdHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey('BaseAd', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.ad.title}"



