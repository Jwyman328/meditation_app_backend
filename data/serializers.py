from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest, userAdditions, MeditationCatagoryType, MeditationCourse, AudioMeditation, MeditationCatagoryType, UserCatagories

from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

class friendRequestSerializer(serializers.ModelSerializer):

    sender_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        "Return sender username"

        return obj.sender.username


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
            newUser = User.objects.create_user(**validated_data) # username=username,password=password
            return newUser
        else:
            return 'error' # not a valid error will need changing 

    class Meta:
        model = User
        fields = ('token','username', 'password' )
