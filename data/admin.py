from django.contrib import admin

# Register your models here.
from .models import AudioMeditation, MeditationCatagoryType, MeditationCourse, UserCatagories, userAdditions

admin.site.register(AudioMeditation)
admin.site.register(MeditationCatagoryType)
admin.site.register(MeditationCourse)
admin.site.register(UserCatagories)
admin.site.register(userAdditions)


