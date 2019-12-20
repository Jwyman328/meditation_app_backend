from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MeditationCatagoryType, MeditationCourse, AudioMeditation, MeditationCatagoryType, UserCatagories

class MeditationCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeditationCourse
        fields = "__all__"


class AudioMeditationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioMeditation
        fields = "__all__"

class UserCatagorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCatagories
        fields = "__all__"
