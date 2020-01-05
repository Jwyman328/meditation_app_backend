from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userAdditions(models.Model):
    """A model that will represent the user model because we don't want to override it """
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    friends =  models.ManyToManyField(User,  blank=True, related_name='user_friends')
    user_photo = models.TextField(blank=True, null=True) # url to photo here 

class MeditationCatagoryType(models.Model):
    """Catagory type for meditations.
    Example: Expert, Begginer, Anxiety

    Keyword Arguments
    -----------------
    name -- name or title of the meditation catagory.

    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class UserCatagories(models.Model):
    """ currently unused """
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    filter_meditation_type_catagories = models.ManyToManyField(MeditationCatagoryType)


class MeditationCourse(models.Model):
    """
    The Meditation Course that contains meditations.


    Keyword Arguments:
    course_id -- the letter id for the course
    title -- title of the meditation course
    image_uri -- url link to a image for the course
    catagories -- a list of MeditationCatagoryType models refering to this meditation course
    favorited_by -- a list of users who currently have this course as a favorite course

    """
    course_id = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    image_uri = models.TextField()
    catagories = models.ManyToManyField(MeditationCatagoryType)
    favorited_by = models.ManyToManyField(User,  blank=True, related_name='user_favourite')
    
    def __str__(self):
        return self.title

class AudioMeditation(models.Model):
    """
    Individual audio meditations

    Keyword Arguments
    -----------------
    orderNumber -- the order of this meditation in it's meditation course
    title -- the title of the meditation
    time -- the amount of time in seconds of the length of the meditation
    author -- the author of the meditation
    image_source --X (currently unused)
    audio_uri -- X (currently unused)
    course -- the meditation course that this meditation is in

     """
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

    


    