from django.contrib import admin

# Register your models here.
from .models import FriendRequest, JournalEntry, AudioMeditation, MeditationCatagoryType, MeditationCourse, UserCatagories, userAdditions

admin.site.register(AudioMeditation)
admin.site.register(MeditationCatagoryType)
admin.site.register(MeditationCourse)
admin.site.register(UserCatagories)
admin.site.register(userAdditions)
admin.site.register(JournalEntry)
admin.site.register(FriendRequest)




