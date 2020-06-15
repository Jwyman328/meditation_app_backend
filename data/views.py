from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import JournalEntry, FitnessGoals, MyFeelings, DirectMessage, FriendRequest, userAdditions, MeditationCourse, AudioMeditation, UserCatagories, MeditationCatagoryType, MeditationListenResults
from django.contrib.auth.models import User

from .serializers import userAdditionsSerializerProfileData, userJournalMoodSerializer, userJournalSerializer, FitnessGoalsSerializer, MyFeelingsSerializer, DirectMessageSerializer, friendRequestSerializer, userAdditionsSerializer, UserSerializer, MeditationCourseSerializer, AudioMeditationSerializer, UserCatagorySerializer, sign_up_serializer
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
        file_path = os.path.join(BASE_DIR, 'media/documents/PositiveSelf.mp3')
        FilePointer = open(file_path)
        files = open(file_path, "rb").read()
        response = HttpResponse(files, content_type="audio/mpeg")
        # this decides what the downloaded filename will be
        response['Content-Disposition'] = 'attachment; filename=filename.mp3'
        return response


class MoodData(views.APIView):
    """
    Return user mood data for week, and month with date ranges.

    Data will be a list of three lists.
    List one: list of mood values from today to a week ago. Ex.[1,2,4,5,3,2,1]
    List two: list of mood values from today to a month ago. Ex [1,4,5,3,2,3,2,3,2,3,2,3,1,1,1]
    List three: list of three date values, today, date a week ago, date a month ago. Ex.[
                "2020-01-29T16:42:20.828910",
                "2020-01-22T16:42:20.828910",
                "2019-12-30T16:42:20.828910"
            ]

    """

    def get(self, request, timeframe):
        today = datetime.datetime.now()
        last_week = today - timedelta(days=7)
        user = request.user
        userJournals = JournalEntry.objects.filter(
            user=user).filter(date__gte=last_week)
        serialized_data = userJournalMoodSerializer(
            userJournals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class JournalEntries(views.APIView):
    """Return a list of all user journal entries and post new journal entries."""

    def get(self, request):
        """Return a list of all user journal entries.

            Entry object will include id, text, mood,date and userId.

            Example:
            [
                {
                    "id": 1,
                    "text": "This is hte first Journal entry",
                    "mood": 4,
                    "date": "2020-01-06",
                    "user": 1
                },
            ]

        """
        user = request.user
        userJournals = JournalEntry.objects.filter(user=user)
        serialized_data = userJournalSerializer(userJournals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

    def post(self, request):
        """Post new journal entries.
            Data posted as json containing text, mood, date.

            Example:
                {"text": "second entry", "mood": "2", "date": "2020-01-08"}

        """

        user = request.user
        data = request.data
        text = data['text']
        mood = data['mood']
        date = data['date']

        journalEntry = JournalEntry.objects.create(
            user=user, text=text, mood=mood, date=date)
        journalEntry.save()

        return Response('Journal created', status.HTTP_201_CREATED)


class ChangeDailyStepGoal(views.APIView):
    """Change user daily step goal to passed newDailySteps url variable """

    def get(self, request, newDailySteps):
        user = request.user
        user_fitness_goals = FitnessGoals.objects.filter(
            user=user).update(daily_step_goal=newDailySteps)
        user_fitness_goals = FitnessGoals.objects.filter(user=user)
        serialized_data = FitnessGoalsSerializer(
            user_fitness_goals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class GetDailyStepGoal(views.APIView):
    """Return user's daily step goal

    Example:
    [
        {
            "id": 1,
            "daily_step_goal": 3006,
            "user": 1
        }
    ]
    """

    def get(self, request):
        user = request.user
        user_fitness_goals = FitnessGoals.objects.filter(user=user)
        serialized_data = FitnessGoalsSerializer(
            user_fitness_goals,  many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class GetMyFeelings(views.APIView):
    """Return and post users current feelings values."""
    def get(self, request):
        """ Return user feelings data
        Example:
            [
                {
                    "id": 156,
                    "depressed": 5,
                    "anxious": 4,
                    "lost": 3,
                    "stressed": 5,
                    "excited": 4,
                    "user": 1
                }
            ]
        """
        user = request.user
        user_feelings = MyFeelings.objects.filter(user=user)
        serialized_data = MyFeelingsSerializer(user_feelings, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

    def post(self, request):
        """ Accept new feelings data.
        
        Example:
            {
            "depressed": "1",
            "anxious": "1",
            "lost": "1",
            "stressed": "1",
            "excited": "1"

            }
        """
        user = request.user
        data = request.data
        depressed = data['depressed']
        anxious = data['anxious']
        lost = data['lost']
        stressed = data['stressed']
        excited = data['excited']

        # delete old feelings obj

        user_feelings = MyFeelings.objects.filter(user=user)
        # delete the previous user feelings data
        if user_feelings:
            user_feelings[0].delete()
        else:
            pass
        # set new user feelings data
        newFeelingsObj = MyFeelings.objects.create(depressed=depressed, anxious=anxious, lost=lost,
                                                   stressed=stressed, excited=excited, user=user)
        newFeelingsObj.save()
        return Response('feelings updated', status.HTTP_201_CREATED)


class CreateMessage(views.APIView):
    """ Post new user message.

        Example:
        {
            "msg":"message",
            "reciever_username": "emnd"
        } 
    """

    def post(self, request):

        user = request.user
        data = request.data
        data['user'] = user

        message = data['msg']
        reciever_username = data['reciever_username']

        # this could be from id or username
        reciever_obj = User.objects.filter(username=reciever_username)
        reciever_obj = reciever_obj[0]

        msg = DirectMessage.objects.create(
            sender_of_msg=user, reciever_of_msg=reciever_obj, msg=message)
        msg.save()

        return Response('message create', status.HTTP_201_CREATED)


class GetDirectMessageConversation(views.APIView):
    """Return the message history between two users

        Example:
        [
            {
                "id": 44,
                "sender_username": "test1",
                "reciever_username": "test2",
                "time_sent": "2020-01-24T19:28:19.799521Z",
                "msg": "Hi my friend",
                "sender_of_msg": 1,
                "reciever_of_msg": 5
            },
            {
                "id": 45,
                "sender_username": "test1",
                "reciever_username": "test2",
                "time_sent": "2020-01-24T19:28:26.760541Z",
                "msg": "How are you ?",
                "sender_of_msg": 1,
                "reciever_of_msg": 5
            },
        ]
    
    """
    def get(self, request, reciever_username):
        user = request.user
        # get the other user in the conversation
        reciever_obj = User.objects.filter(username=reciever_username)
        reciever_obj = reciever_obj[0]
        # get all messages sent by current user to other user
        conversation_history_of_current_user = DirectMessage.objects.filter(
            sender_of_msg=user).filter(reciever_of_msg=reciever_obj)

        # get all messages sent by other user to current user
        conversation_history_of_reciever = DirectMessage.objects.filter(
            sender_of_msg=reciever_obj).filter(reciever_of_msg=user)

        # Combine messages sent to by current and other user to each other 
        full_conversation = conversation_history_of_current_user | conversation_history_of_reciever
        
        # order the conversation from oldest to newest
        full_conversation_ordered = full_conversation.order_by('time_sent')

        serialized_data = DirectMessageSerializer(
            full_conversation_ordered, many=True).data

        return Response(serialized_data, status.HTTP_200_OK)


class acceptDenyFriendRequest(views.APIView):
    """Handle acceptance or denial of friend request.
    
    If accepted add each user to other's friend list.
    Always delete friend request.
    """
    def get(self, request, id, Bool):
        user = request.user
        pending_friend_request = FriendRequest.objects.get(id=id)

        if bool(Bool):
            pending_friend_request.status = bool(Bool)
            pending_friend_request.save()

            # add to both of their friend lists
            sender = pending_friend_request.sender
            # sender_id = pending_friend_request.sender.id
            senderUserAdditions = userAdditions.objects.filter(user=sender)
            newFriendList = senderUserAdditions[0].friends.add(user)
            senderUserAdditions[0].save()

            userUserAdditions = userAdditions.objects.filter(user=user)
            newFriendList2 = userUserAdditions[0].friends.add(sender)
            userUserAdditions[0].save()
            pending_friend_request.delete()
            return Response('updated', status.HTTP_200_OK)
        else:
            # if the user rejects the request remove it from the friend requests
            pending_friend_request.delete()
            return Response('updated', status.HTTP_200_OK)


class pendingFriendRequests(views.APIView):
    """Return list of all pending(unreject/unaccepted) friend requests sent to current user 

        Example:
        [
            {
                "id": 32,
                "sender_username": "test2",
                "sender_profile_picture": "userphoto",
                "status": false,
                "sender": 123,
                "reciever": 1
            }
        ]
    
    """
    def get(self, request):
        user = request.user
        pending_friend_request = FriendRequest.objects.filter(
            reciever=user).filter(status=False)
        serialized_data = friendRequestSerializer(
            pending_friend_request, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class sendFriendRequest(views.APIView):
    """Create friend request object from user to reciever_username"""
    def get(self, request, reciever_username):
        user = request.user
        reciever = User.objects.filter(username=reciever_username)
        reciever = reciever[0]
        data = [user, reciever]
        # check if the reicever is already this persons friend
        this_user = userAdditions.objects.filter(user=user)
        if reciever.id in this_user[0].friends.values_list(flat=True):
            return Response('already your friend', status.HTTP_400_BAD_REQUEST)
        else:
            pass

        this_user_pending_request = FriendRequest.objects.filter(sender=user)
        # check if user already has a pendign request to this person
        for pending_request in this_user_pending_request:
            if pending_request.reciever == reciever:
                return Response('you already sent this guy a friend request', status.HTTP_400_BAD_REQUEST)
        else:
            pass

        newFriendRequest = FriendRequest.objects.create(
            sender=data[0], reciever=data[1])
        newFriendRequest.save()
        serialized_data = friendRequestSerializer(newFriendRequest)
        if serialized_data:
            print('in')
            return Response(serialized_data.data, status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class addRemoveFriend(views.APIView):
    # add a friend to friends list
    def get(self, request, friend_user_name):
        user = request.user
        user_id = user.id
        # friend_user_object = User.objects.get(int(friend_user_id))
        friend_user_object = User.objects.filter(username=friend_user_name)
        friend_user_object = friend_user_object[0]
        friend_user_id = friend_user_object.id

        # check if it is already in it and then remove it if it is

        user_to_add_to_friends = userAdditions.objects.filter(id=user_id)
        if friend_user_id in user_to_add_to_friends[0].friends.values_list(flat=True):
            new_friends_list = user_to_add_to_friends[0].friends.remove(
                friend_user_object)  # may need the friend user model not just id number
            user_to_add_to_friends[0].save()  # maybe use this
            # new_friends_list.save()
        else:
            new_friends_list = user_to_add_to_friends[0].friends.add(
                friend_user_object)
            user_to_add_to_friends[0].save()
        # (course_to_favorite[0].favorited_by.values_list(flat=True), 'heat')

        my_query = userAdditions.objects.filter(user=request.user)
        serialized_data = userAdditionsSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)
        # serialized_data = addFavoriteMeditationCourseSerializer(my_query, many=True).data


class getMyFriends(views.APIView):
    """Return a list of the user's friends
    
    Example:
    [
        {
            "username": "test2",
            "first_name": "first",
            "last_name": "last",
            "user_photo": "photoUrl"
        },
        {
            "username": "test3",
            "first_name": "first",
            "last_name": "last",
            "user_photo": "photourl"
        }
    ]
    """

    def get(self, request):
        my_query = userAdditions.objects.filter(user=request.user)

        # serialized_data = userAdditionsSerializer(my_query, many=True).data
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
        my_query = MeditationCourse.objects.filter(favorited_by=user_id)
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

    def get(self, request, course_id):
        user = request.user
        user_id = user.id
        # check if it is already in it and then remove it if it is

        course_to_favorite = MeditationCourse.objects.filter(id=course_id)
        if user_id in course_to_favorite[0].favorited_by.values_list(flat=True):
            new_favorite_list = course_to_favorite[0].favorited_by.remove(user)
            course_to_favorite[0].save()
        else:
            new_favorite_list = course_to_favorite[0].favorited_by.add(user)
            course_to_favorite[0].save()
        # (course_to_favorite[0].favorited_by.values_list(flat=True), 'heat')

        my_query = MeditationCourse.objects.filter(favorited_by=user_id)
        serialized_data = MeditationCourseSerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)
        # serialized_data = addFavoriteMeditationCourseSerializer(my_query, many=True).data


class getCatagoryMeditationCourses(views.APIView):
    """Currently unused """

    def get(self, request):
        user = request.user
        my_query = UserCatagories.objects.filter(user=user)
        serialized_data = UserCatagorySerializer(my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class get_profile_additional_data(views.APIView):
    """Return user's userAdditions data
    
    Example:
        [
            {
                "first_name": "testFirst",
                "last_name": "testLast",
                "weight": 197,
                "height_feet": 5,
                "height_inches": 11,
                "gender": "Male",
                "birth_year": 1947,
                "birth_month": 12
            }
        ]
    """
    def get(self, request):
        user = request.user
        my_query = userAdditions.objects.filter(user=user)
        serialized_data = userAdditionsSerializerProfileData(
            my_query, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class sign_up_set_health_additional_data(views.APIView):
    """Add user health data to user_additions on signup
    
    Additional data to data includes, heigh, weight, gender, and DOB.
     
    """
    def post(self, request):
        health_data = request.data
        user = request.user
        my_query = userAdditions.objects.filter(user=user)
        this_user_additions = my_query[0]
        this_user_additions.weight = health_data['weight']
        this_user_additions.height_feet = health_data['height']['feet']
        this_user_additions.height_inches = health_data['height']['inch']
        this_user_additions.gender = health_data['gender']
        this_user_additions.birth_year = health_data['DOB']['year']
        this_user_additions.birth_month = health_data['DOB']['month']
        this_user_additions.save()

        if this_user_additions:
            return Response('health data for user added', status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class sign_up_additional_data(views.APIView):
    """Create userAdditions object for user on signup """

    def post(self, request):
        firstName_lastName = request.data
        user = request.user
        my_query = userAdditions.objects.filter(user=user)
        this_user_additions = my_query[0]
        this_user_additions.first_name = firstName_lastName['first_name']
        this_user_additions.last_name = firstName_lastName['last_name']
        this_user_additions.save()

        # automativally create a fitness goal set to 10000 steps
        FitnessGoals.objects.create(user=user)

        if this_user_additions:
            return Response('first name last name added', status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class sign_up_user(views.APIView):
    """Create a new user with passed username and password."""

    # allow anyone to access the ability to make a user
    permission_classes = [AllowAny]

    def post(self, request):
        username_password = request.data
        serialized_data = sign_up_serializer(data=username_password)
        if serialized_data.is_valid():
            # make a user additions for this user
            serialized_data.save()
            return Response(serialized_data.data, status.HTTP_201_CREATED)
        else:
            return Response('error', status.HTTP_400_BAD_REQUEST)


class ResetPassWord(views.APIView):
    """Send reset password email to user."""

    permission_classes = [AllowAny]

    def get(self, request, email):

        msg = 'Click to start reset password process http://intense-gorge-29567.herokuapp.com/accounts/password_reset/'  # + new_password

        all_users = User.objects.all()
        email_sent = False
        for user in all_users:
            if email == user.email:
                send_mail('New password Meditation App', msg,
                          'MeditationApp@dev.com', [email], fail_silently=False)
                email_sent = True
                return Response('email sent', status.HTTP_201_CREATED)
            else:
                None

        if email_sent:
            None
        else:
            return Response('email does not exist', status.HTTP_404_NOT_FOUND)

class RecordMeditationListened(views.APIView):

    def post(self, request):
        meditation_data = request.data
        meditation_name = meditation_data["meditation_name"] 
        meditation_amount_time_listened = meditation_data["meditation_amount_time_listened"]

        newMeditationListenResults = MeditationListenResults.objects.create(meditation_amount_time_listened=meditation_amount_time_listened,
        meditation_name=meditation_name
        )
        newMeditationListenResults.save()

        return Response('Meditation Recorded', status.HTTP_201_CREATED)




