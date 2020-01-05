from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import userAdditions, MeditationCourse, AudioMeditation, UserCatagories, MeditationCatagoryType
from django.contrib.auth.models import User

from .serializers import userAdditionsSerializer, UserSerializer, MeditationCourseSerializer, AudioMeditationSerializer, UserCatagorySerializer, sign_up_serializer
from rest_framework import status
from rest_framework.permissions import AllowAny


# Create your views here.
class getMyFriends(views.APIView):
    "Return the entire database of users"

    def get(self, request):
        my_query = userAdditions.objects.filter(user=request.user)
        serialized_data = UserSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getAllUsers(views.APIView):
    "Return the entire database of users"

    def get(self, request):
        my_query = User.objects.all()
        serialized_data = UserSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getAllMeditationCourses(views.APIView):
    """Return all meditation Courses """

    def get(self, request):
        my_query = MeditationCourse.objects.all()
        serialized_data = MeditationCourseSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getAllMeditations(views.APIView):
    """Return an individual audio mediation requested by the course_id
    
    Keyword Arguments
    -----------------
    course_id -- the object if of the audio meditation wanted to be returned
    """

    def get(self, request, course_id):
        my_query = AudioMeditation.objects.filter(course=course_id)
        serialized_data = AudioMeditationSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class getFavoritedMeditationCourses(views.APIView):
    """Return a list of meditation courses currently favorited by the current user """

    def get(self, request):
        user = request.user
        user_id = user.id
        my_query = MeditationCourse.objects.filter(favorited_by = user_id)
        serialized_data = MeditationCourseSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class addFavoritedMeditationCourses(views.APIView):
    """Add or remove the meditation course of the course_id for the current user
    
    If the current user is in the favorited_by list of this course_id 
    when the http request is made, then remove the user from the favorited_by list.
    If the current user is not in the favorited_by list of this course_id when 
    the http request is made, then add the user to the favorited_by list.

    In both cases return a list of all meditations favorited_by the current user

    Keyword Arguments
    -----------------
    course_id -- the id of the audio_meditation course

    """

    def get(self, request,course_id):
        user = request.user
        user_id = user.id
        ## check if it is already in it and then remove it if it is 
        
        course_to_favorite = MeditationCourse.objects.filter(id=course_id)
        if user_id in course_to_favorite[0].favorited_by.values_list(flat=True):
            new_favorite_list = course_to_favorite[0].favorited_by.remove(user)
            course_to_favorite[0].save()
        else:
            new_favorite_list = course_to_favorite[0].favorited_by.add(user)
            course_to_favorite[0].save()
        #(course_to_favorite[0].favorited_by.values_list(flat=True), 'heat')

        my_query = MeditationCourse.objects.filter(favorited_by = user_id)
        serialized_data = MeditationCourseSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)
        #serialized_data = addFavoriteMeditationCourseSerializer(my_query, many=True).data
        

class getCatagoryMeditationCourses(views.APIView):
    """Currently unused """

    def get(self, request):
        user = request.user 
        my_query =  UserCatagories.objects.filter(user=user)
        serialized_data = UserCatagorySerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class sign_up_user(views.APIView):
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


