from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MyFeelings(models.Model):
    depressed =  models.PositiveIntegerField(default=0)
    anxious = models.PositiveIntegerField(default=0)
    lost =  models.PositiveIntegerField(default=0)
    stressed =  models.PositiveIntegerField(default=0)
    excited =  models.PositiveIntegerField(default=0)

class DirectMessage(models.Model):
    sender_of_msg = models.ForeignKey(User, related_name='msg_sender', on_delete = models.CASCADE)
    reciever_of_msg = models.ForeignKey(User, related_name='msg_reciever', on_delete = models.CASCADE)
    time_sent = models.DateTimeField(auto_now=True)
    msg = models.TextField(blank=True, null=True)

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date = models.DateField()

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='user_sender', on_delete = models.CASCADE)
    reciever = models.ForeignKey(User, related_name='user_reciever', on_delete = models.CASCADE)
    status = models.BooleanField(default=False)


class userAdditions(models.Model):
    """A model that will represent the user model because we don't want to override it """
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    friends =  models.ManyToManyField(User,  blank=True, related_name='user_friends')
    user_photo = models.TextField(default= 'data:image/jpeg;base64,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' ,
        blank=True, null=True) # url to photo here 

    def __str__(self):
        return self.user.username

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

    


    