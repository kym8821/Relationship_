# Generated by Django 4.2 on 2023-04-13 05:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_remove_blog_liker_blog_liker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='liker',
        ),
        migrations.AddField(
            model_name='blog',
            name='liker',
            field=models.ManyToManyField(related_name='liker', to=settings.AUTH_USER_MODEL),
        ),
    ]
