# Generated by Django 5.1.1 on 2024-09-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(default=12, upload_to=''),
            preserve_default=False,
        ),
    ]
