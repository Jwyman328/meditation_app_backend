from django.contrib import admin

# Register your models here.
from .models import MyFeelings, DirectMessage, FriendRequest, JournalEntry, AudioMeditation, MeditationCatagoryType, MeditationCourse, UserCatagories, userAdditions

admin.site.register(AudioMeditation)
admin.site.register(MeditationCatagoryType)
admin.site.register(MeditationCourse)
admin.site.register(UserCatagories)
admin.site.register(userAdditions)
admin.site.register(JournalEntry)
admin.site.register(FriendRequest)
admin.site.register(DirectMessage)
admin.site.register(MyFeelings)
admin.site.register(FitnessGoals)










