from rest_framework import serializers
from user.models import Profile, Tweet, Comment


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'lastname', 'email', 'username', 'bio', 'tweets', 'created', 'profile_img']

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'content', 'liked', 'created', 'updated']

class CommmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'content', 'tweets', 'parent', 'liked', 'created', 'updated']