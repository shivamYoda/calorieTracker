from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import TrackerUser

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        extra_args = {}
        if self.initial_data['type'] == "admin":
            extra_args['is_staff'] = True
            extra_args['is_superuser'] = True
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], **extra_args)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')

class TrackerUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    type = serializers.CharField()
    expected_calories_per_day = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        tracker_user = TrackerUser.objects.create(user=validated_data['user'], type = validated_data['type'],
                                                  expected_calories_per_day = validated_data['expected_calories_per_day'])
        return tracker_user

    def update(self, instance, validated_data):
        instance.type = validated_data['type']
        instance.expected_calories_per_day = validated_data['expected_calories_per_day']
        instance.save()
        return instance

    class Meta:
        model = TrackerUser
        fields = ('id', 'user', 'type', 'expected_calories_per_day')
