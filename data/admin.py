from django.contrib import admin

# Register your models here.
from .models import audio_field_test, FitnessGoals, MyFeelings, DirectMessage, FriendRequest, JournalEntry, AudioMeditation, MeditationCatagoryType, MeditationCourse, UserCatagories, userAdditions, MeditationListenResults

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
admin.site.register(audio_field_test)
admin.site.register(MeditationListenResults)












