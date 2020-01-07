# Generated by Django 3.0.1 on 2020-01-07 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0006_auto_20200106_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_sent', models.DateTimeField(auto_now=True)),
                ('reciever_of_msg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_reciever', to=settings.AUTH_USER_MODEL)),
                ('sender_of_msg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]