from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import  JournalEntry, FitnessGoals, MyFeelings, DirectMessage, FriendRequest, userAdditions, MeditationCourse, AudioMeditation, UserCatagories, MeditationCatagoryType
from django.contrib.auth.models import User

from .serializers import userJournalMoodSerializer, userJournalSerializer, FitnessGoalsSerializer, MyFeelingsSerializer, DirectMessageSerializer, friendRequestSerializer, userAdditionsSerializer, UserSerializer, MeditationCourseSerializer, AudioMeditationSerializer, UserCatagorySerializer, sign_up_serializer
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.core.mail import send_mail
import datetime
from datetime import timedelta
import os
from django.http import HttpResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
class ReturnAudio(views.APIView):
    """ currently when i make this call i will get hte positive self mp3
       eventually i would want to pass a url variable with the file name and then it would get that file"""
    def get(self, request):
        file_path =  os.path.join(BASE_DIR, 'media/documents/PositiveSelf.mp3')
       
        FilePointer = open(file_path)
        #response = HttpResponse(FilePointer,content_type='application/force-download' )
        #response['Content-Disposition'] = 'attachment; filename=NameOfFile'
        #Content-Disposition: attachment; filename="my-file.mp3"
        #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        #settings
        ## also make the tow folders, media/documents/ put in a file
        #MEDIA_URL = '/media/'
        #MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



        files = open(file_path, "rb").read() 
        response = HttpResponse(files, content_type="audio/mpeg") 
        response['Content-Disposition'] = 'attachment; filename=filename.mp3'  # this decides what the downloaded filename will be 
        return response
        #return response
        #url
        #path('ReturnAudio', views.ReturnAudio.as_view(), name='return_audio'),

        #models
        #class audio_field_test(models.Model):
            #audi_body = models.FileField(upload_to='documents/')


class MoodData(views.APIView):
    # get last 7 days, month or year 
     def get(self, request,timeframe):
        #timeframe is week, month, year
        # todays date 
        today = datetime.datetime.now()
        last_week = today - timedelta(days=7)
        user = request.user
        userJournals = JournalEntry.objects.filter(user=user).filter(date__gte = last_week )
        serialized_data = userJournalMoodSerializer(userJournals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)
        


class JournalEntries(views.APIView):
    # get all the users journal entries
    def get(self, request):
        user = request.user
        userJournals = JournalEntry.objects.filter(user=user)
        serialized_data = userJournalSerializer(userJournals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

    def post(self,request):
        """  "text": "second entry", "mood": "2", "date": "2020-01-08" """

        user = request.user
        data = request.data 
        text = data['text']
        mood = data['mood']
        date = data['date']

        journalEntry = JournalEntry.objects.create(user=user, text=text, mood=mood, date = date)
        journalEntry.save()

        return Response('Journal created', status.HTTP_201_CREATED)

class ChangeDailyStepGoal(views.APIView):
     def get(self, request, newDailySteps):
        user = request.user
        user_fitness_goals = FitnessGoals.objects.filter(user = user).update(daily_step_goal=newDailySteps)
        user_fitness_goals = FitnessGoals.objects.filter(user = user)
        serialized_data = FitnessGoalsSerializer(user_fitness_goals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

class GetDailyStepGoal(views.APIView):

    def get(self, request):
        user = request.user
        user_fitness_goals = FitnessGoals.objects.filter(user = user)
        serialized_data = FitnessGoalsSerializer(user_fitness_goals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class GetMyFeelings(views.APIView):

    def get(self, request):
        user = request.user
        user_feelings = MyFeelings.objects.filter(user = user)
        serialized_data = MyFeelingsSerializer(user_feelings, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

    def post(self, request):
        """ post must be {
   
        "depressed": "1",
        "anxious": "1",
        "lost": "1",
        "stressed": "1",
        "excited": "1"
      
        }
        """ 
        user = request.user
        data = request.data
        depressed=data['depressed']
        anxious = data['anxious']
        lost = data['lost']
        stressed = data['stressed']
        excited = data['excited']

        # delete old feelings obj 
        
        user_feelings = MyFeelings.objects.filter(user = user)
        if user_feelings:
            user_feelings[0].delete()
        else:
            pass

        newFeelingsObj = MyFeelings.objects.create(depressed=depressed , anxious=anxious,lost=lost ,
            stressed=stressed, excited=excited, user=user)
        newFeelingsObj.save()

        return Response('feelings updated', status.HTTP_201_CREATED)



class CreateMessage(views.APIView):
    """ post must be {
        "msg":"message",
        "reciever_username": "emnd"} """ 

    def post(self,request):

        user = request.user
        data = request.data 
        data['user'] = user

        message = data['msg']
        reciever_username = data['reciever_username']
        
        reciever_obj = User.objects.filter(username = reciever_username) #this could be from id or username
        reciever_obj = reciever_obj[0]

        msg = DirectMessage.objects.create(sender_of_msg=user, reciever_of_msg=reciever_obj, msg=message)
        msg.save()

        return Response('message create', status.HTTP_201_CREATED)

        




class GetDirectMessageConversation(views.APIView):
    """Get the message history between the two """
    def get(self, request, reciever_username):
        user = request.user
        reciever_obj = User.objects.filter(username = reciever_username) #this could be from id or username
        reciever_obj = reciever_obj[0]

        conversation_history_of_current_user = DirectMessage.objects.filter(sender_of_msg =user).filter(reciever_of_msg=reciever_obj)

        conversation_history_of_reciever = DirectMessage.objects.filter(sender_of_msg=reciever_obj).filter(reciever_of_msg=user)
        
        full_conversation = conversation_history_of_current_user |  conversation_history_of_reciever
        full_conversation_ordered = full_conversation.order_by('time_sent')

        serialized_data = DirectMessageSerializer(full_conversation_ordered , many=True).data

        return Response(serialized_data, status.HTTP_200_OK)
        



class acceptDenyFriendRequest(views.APIView):
    def get(self, request, id, Bool):
        user = request.user
        pending_friend_request = FriendRequest.objects.get(id=id)
        
        if bool(Bool):
            pending_friend_request.status= bool(Bool)
            pending_friend_request.save()

            # add to both of their friend lists
            sender = pending_friend_request.sender
            #sender_id = pending_friend_request.sender.id
            senderUserAdditions = userAdditions.objects.filter(user = sender )
            newFriendList = senderUserAdditions[0].friends.add(user)
            senderUserAdditions[0].save()

            userUserAdditions = userAdditions.objects.filter(user = user)
            newFriendList2 = userUserAdditions[0].friends.add(sender)
            userUserAdditions[0].save()
            pending_friend_request.delete()  
            return Response('updated', status.HTTP_200_OK)
        else:
            # if the user rejects the request remove it from the friend requests 
            pending_friend_request.delete()
            return Response('updated', status.HTTP_200_OK)





class pendingFriendRequests(views.APIView):
    def get(self, request):
        user = request.user
        pending_friend_request = FriendRequest.objects.filter(reciever = user).filter(status=False)
        serialized_data = friendRequestSerializer(pending_friend_request, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)




class sendFriendRequest(views.APIView):
   
   def get(self,request, reciever_username):
        user = request.user
        reciever = User.objects.filter(username = reciever_username)
        reciever = reciever[0]
        data = [user, reciever]
        # check if the reicever is already this persons friend
        this_user = userAdditions.objects.filter(user = user)
        if reciever.id in this_user[0].friends.values_list(flat=True):
            return Response('already your friend', status.HTTP_400_BAD_REQUEST)
        else:
            pass
        
        this_user_pending_request = FriendRequest.objects.filter(sender=user)
        # check if user already has a pendign request to this person
        for pending_request in  this_user_pending_request:
            if pending_request.reciever == reciever:
                return Response('you already sent this guy a friend request', status.HTTP_400_BAD_REQUEST)

        else:
            pass
        
        newFriendRequest = FriendRequest.objects.create(sender=data[0],reciever=data[1] )
        newFriendRequest.save()
        serialized_data = friendRequestSerializer(newFriendRequest)
        if serialized_data:
            print('in')
            return Response(serialized_data.data,status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class addRemoveFriend(views.APIView):
    ##add a friend to friends list
    def get(self, request,friend_user_name):
        user = request.user
        user_id = user.id
        #friend_user_object = User.objects.get(int(friend_user_id))
        friend_user_object = User.objects.filter(username = friend_user_name)
        friend_user_object =friend_user_object[0]
        friend_user_id = friend_user_object.id

        ## check if it is already in it and then remove it if it is 
        
        user_to_add_to_friends = userAdditions.objects.filter(id=user_id)
        if friend_user_id in user_to_add_to_friends[0].friends.values_list(flat=True):
            new_friends_list = user_to_add_to_friends[0].friends.remove(friend_user_object) # may need the friend user model not just id number
            user_to_add_to_friends[0].save()  #maybe use this 
            ##new_friends_list.save()
        else:
            new_friends_list = user_to_add_to_friends[0].friends.add(friend_user_object)
            user_to_add_to_friends[0].save()
        #(course_to_favorite[0].favorited_by.values_list(flat=True), 'heat')

        my_query = userAdditions.objects.filter(user=request.user)
        serialized_data = userAdditionsSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)
        #serialized_data = addFavoriteMeditationCourseSerializer(my_query, many=True).data
        

class getMyFriends(views.APIView):
    "Return a list of the user's friends"

    def get(self, request):
        my_query = userAdditions.objects.filter(user=request.user)

        #serialized_data = userAdditionsSerializer(my_query, many=True).data
        serialized_data = UserSerializer(my_query[0].friends, many=True).data
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
            # make a user additions for this user 
            serialized_data.save()
            return Response(serialized_data.data,status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class ResetPassWord(views.APIView):

    permission_classes = [AllowAny]

    def get(self, request, email):
        #length = 13
        #chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        #random.seed = (os.urandom(1024))
        #new_password = ('tom'.join(random.choice(chars) for i in range(length)))

        #user = userAdditions.objects.filter(email=email)
        #user = user[0]
       
        msg = 'Click to start reset password process http://intense-gorge-29567.herokuapp.com/accounts/password_reset/' #+ new_password
        
        send_mail('New password Meditation App', msg, 'MeditationApp@dev.com', [email], fail_silently=False)
        return Response('hi',status.HTTP_201_CREATED)





