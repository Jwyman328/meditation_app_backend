# Generated by Django 3.0.1 on 2020-01-14 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_myfeelings_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradditions',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='useradditions',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
