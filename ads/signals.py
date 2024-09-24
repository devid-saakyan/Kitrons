from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BaseAd, SurveyAd, VideoAd, PostAd


@receiver(post_save, sender=BaseAd)
def create_related_ad(sender, instance, created, **kwargs):
    if created:
        if instance.ad_type == 'survey':
            SurveyAd.objects.create(
                title=instance.title,
                description=instance.description,
                company=instance.company,
                category=instance.category,
                photo=None
            )
        elif instance.ad_type == 'video':
            VideoAd.objects.create(
                title=instance.title,
                description=instance.description,
                company=instance.company,
                category=instance.category,
                video=None
            )
        elif instance.ad_type == 'post':
            PostAd.objects.create(
                title=instance.title,
                description=instance.description,
                company=instance.company,
                category=instance.category,
                post_text=None,
                photo=None
            )
