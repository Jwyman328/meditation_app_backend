# Generated by Django 3.0.1 on 2020-01-05 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_useradditions'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradditions',
            name='user_photo',
            field=models.TextField(blank=True, null=True),
        ),
    ]