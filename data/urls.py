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
from django.urls import path
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
    path('friends/message_history/<int:reciever_id>/', views.GetDirectMessageConversation.as_view(), name = 'get_conversation'),
]
