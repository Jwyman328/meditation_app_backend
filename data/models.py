from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MeditationCatagoryType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class UserCatagories(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    filter_meditation_type_catagories = models.ManyToManyField(MeditationCatagoryType)


class MeditationCourse(models.Model):
    course_id = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    image_uri = models.TextField()
    catagories = models.ManyToManyField(MeditationCatagoryType)
    favorited_by = models.ManyToManyField(User,  blank=True, related_name='user_favourite')
    
    def __str__(self):
        return self.title

class AudioMeditation(models.Model):
    orderNumber = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    time = models.PositiveIntegerField() #time representation in seconds
    author = models.CharField(max_length=150)
    # uri:  require('../audio/CapableChange.mp3'),
    image_source = models.TextField()
    audio_uri = models.TextField(blank=True,null=True, default=None)
    course = models.ForeignKey(MeditationCourse,blank=True,null=True,  on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    


    