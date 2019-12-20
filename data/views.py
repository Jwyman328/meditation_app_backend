from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import MeditationCourse, AudioMeditation, UserCatagories, MeditationCatagoryType

from .serializers import MeditationCourseSerializer, AudioMeditationSerializer, UserCatagorySerializer
from rest_framework import status


# Create your views here.

class getAllMeditationCourses(views.APIView):

    def get(self, request):
        my_query = MeditationCourse.objects.all()
        serialized_data = MeditationCourseSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getAllMeditations(views.APIView):

    def get(self, request, course_id):
        my_query = AudioMeditation.objects.filter(course=course_id)
        serialized_data = AudioMeditationSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getFavoritedMeditationCourses(views.APIView):

    def get(self, request):
        user = request.user
        user_id = user.id
        my_query = MeditationCourse.objects.filter(favorited_by = user_id)
        serialized_data = MeditationCourseSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getCatagoryMeditationCourses(views.APIView):
    # get the UserCatagories that has to do with this user 
    ## then get the cataogires from that 

    def get(self, request):
        user = request.user 
        my_query =  UserCatagories.objects.filter(user=user)
        serialized_data = UserCatagorySerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)





