# Generated by Django 2.2.7 on 2019-12-19 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20191218_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meditationcourse',
            name='catagories',
        ),
        migrations.AddField(
            model_name='meditationcourse',
            name='catagories',
            field=models.ManyToManyField(to='data.MeditationCatagoryType'),
        ),
    ]