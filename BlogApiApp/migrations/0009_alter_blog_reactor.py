# Generated by Django 4.1.7 on 2023-03-22 13:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BlogApiApp', '0008_comment_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='reactor',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
