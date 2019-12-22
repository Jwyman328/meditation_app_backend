from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import MeditationCourse, AudioMeditation, UserCatagories, MeditationCatagoryType

from .serializers import MeditationCourseSerializer, AudioMeditationSerializer, UserCatagorySerializer
from rest_framework import status
from rest_framework.permissions import AllowAny


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



class sign_up_user(APIView):
    """Create a new user with passed username and password."""

    # allow anyone to access the ability to make a user
    permission_classes = [AllowAny]

    def post(self,request):
        username_password = request.data 
        serialized_data = sign_up_serializer(data = username_password)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


