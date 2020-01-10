from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FitnessGoals, MyFeelings, DirectMessage, FriendRequest, userAdditions, MeditationCatagoryType, MeditationCourse, AudioMeditation, MeditationCatagoryType, UserCatagories

from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

class FitnessGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoals
        fields =  "__all__"


class MyFeelingsSerializer(serializers.ModelSerializer):

     class Meta:
        model = MyFeelings
        fields =  "__all__"

class CreateMessageSerializer(serializers.ModelSerializer):
 
 
 def create(self, validated_data):
    """create a User object if username and password validated."""
    message = validated_data['msg']
    reciever_username = validated_data['reciever']

    reciever_obj = User.objects.filter(username = reciever_username) #this could be from id or username
    reciever_obj = reciever_obj[0]

    if True:
        newUser = DirectMessage.objects.create(**validated_data) # username=username,password=password
        return newUser
    else:
        return 'error' # not a valid error will need changing 

    class Meta:
        model = User
        fields = ('token','username', 'password' )


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    reciever_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
            "Return sender username"
            return obj.sender_of_msg.username

    def get_reciever_username(self, obj):
            "Return sender username"
            return obj.reciever_of_msg.username

    class Meta:
            model = DirectMessage
            fields =  "__all__"


class friendRequestSerializer(serializers.ModelSerializer):

    sender_username = serializers.SerializerMethodField()
    sender_profile_picture = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        "Return sender username"

        return obj.sender.username

    def get_sender_profile_picture(self, obj):
        "Return sender username"
        this_obj_userAdditions = userAdditions.objects.filter(user = obj.sender)
        user_photo = this_obj_userAdditions[0].user_photo
        return user_photo



    class Meta:
        model = FriendRequest
        fields =  "__all__"


class userAdditionsSerializer(serializers.ModelSerializer):
    """Serialize list of friends """
    class Meta:
        model = userAdditions
        fields = ["friends"] # probably change to jsut username 


class UserSerializer(serializers.ModelSerializer):
    user_photo = serializers.SerializerMethodField()

    def get_user_photo(self, obj):
        "Return user photo"
        this_obj_userAdditions = userAdditions.objects.filter(user = obj)
        user_photo = this_obj_userAdditions[0].user_photo
        return user_photo


    class Meta:
        model = User
        fields = ("username",'first_name', 'last_name', 'user_photo') # probably change to jsut username 


class MeditationCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeditationCourse
        fields = "__all__"


class AudioMeditationSerializer(serializers.ModelSerializer):
    meditation_course_photo = serializers.SerializerMethodField()

    def get_meditation_course_photo(self, obj):
        "Return user photo"
        this_obj_meditation_course_image = obj.course.image_uri
        return this_obj_meditation_course_image

    class Meta:
        model = AudioMeditation
        fields = "__all__"
    

class UserCatagorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCatagories
        fields = "__all__"


class sign_up_serializer(serializers.ModelSerializer):
    """Create a new user and return associated jwt token.
    The password and username will be validated only for length.
    
    Keyword Arguments
    -----------------
    password: password takenfrom the users post when signing up
    token: JWT token created for new user
    Methods
    ------------
    get_token:
        Create a unique JWT token for the user to use with thier requests.
    create:
        create a User object if username and password validated.
    """
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        """Create a unique JWT token for the user to use with thier requests."""

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """create a User object if username and password validated."""
        username = validated_data['username']
        password = validated_data['password']

        if len(username) > 5 and len(password) > 5:
            newUser = User.objects.create_user(email = username, **validated_data) # username=username,password=password
                        # make a user additions for this user 
          
            new_user_additions = userAdditions.objects.create(user=newUser)
            new_user_additions.save()
            return newUser
        else:
            return 'error' # not a valid error will need changing 

    class Meta:
        model = User
        fields = ('token','username', 'password' )


