"""meditation_app_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('all_meditation_courses/', views.getAllMeditationCourses.as_view(), name='all_meditation_courses'),
    path('course_meditations/<int:course_id>/',views.getAllMeditations.as_view(), name='all_meditations_for_course' ),
    path('course_meditations/favorited', views.getFavoritedMeditationCourses.as_view(), name = 'favorited_Meditation_Courses'),
    path('course_meditations/add_favorite_course/<int:course_id>/', views.addFavoritedMeditationCourses.as_view(), name = 'add_favorite_meditation_course'),
    path('course_meditations/filtered', views.getCatagoryMeditationCourses.as_view(), name='filtered_courses'),
    path('all_users', views.getAllUsers.as_view(), name = 'all_users'),
    path('user_friends', views.getMyFriends.as_view(), name='user_friends'),
    path('friends/addRemoveFriend/<str:friend_user_name>/',views.addRemoveFriend.as_view(), name='add_remove_friend'),
    path('friends/sendFriendRequest/<str:reciever_username>/',views.sendFriendRequest.as_view(), name='send_friend_request'),
    path('friends/pending_friend_requests/', views.pendingFriendRequests.as_view(), name='pending_friend_requests'),
    path('friends/<int:id>/<int:Bool>/', views.acceptDenyFriendRequest.as_view(), name = 'accept_deny_friend_request'),
    path('friends/message_history/<str:reciever_username>/', views.GetDirectMessageConversation.as_view(), name = 'get_conversation'),
    path('friends/create_message/', views.CreateMessage.as_view(), name = 'create_message'),
    path('personal/GetMyFeelings/', views.GetMyFeelings.as_view(), name = 'get_my_feelings'),
    path('resetPassword/<str:email>/', views.ResetPassWord.as_view(), name = 'resetPassword'),
    path('fitness/dailyStepGoal/', views.GetDailyStepGoal.as_view(), name = 'GetDailyStepGoal'),
    path('fitness/changeDailyStepGoal/<int:newDailySteps>',views.ChangeDailyStepGoal.as_view(), name='ChangeDailyStepGoal'),
    path('Journal/all_user_entries', views.JournalEntries.as_view(), name='JournalEntries'),
    path('Journal/last_week_moods/<str:timeframe>', views.MoodData.as_view(), name='last_week_moods'),
    path('ReturnAudio', views.ReturnAudio.as_view(), name='return_audio'),
    path('sign_up_additional_data', views.sign_up_additional_data.as_view(), name='sign_up_additional_data'),
    path('sign_up_set_health_additional_data', views.sign_up_set_health_additional_data.as_view(), name='sign_up_set_health_additional_data'),
    path('get_profile_additional_data', views.get_profile_additional_data.as_view(), name="get_profile_additional_data"),

]
