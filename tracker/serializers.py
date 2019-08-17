from rest_framework import serializers
from trackerUser.serializers import TrackerUserSerializer
from .models import TrackerEntry
import datetime

class TrackerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = TrackerUserSerializer(read_only=True)
    calories = serializers.IntegerField()
    text = serializers.CharField(max_length=100)
    date = serializers.DateField(default=datetime.datetime.now().date())
    time = serializers.TimeField(default=datetime.datetime.now().time())
    less_than_calories_per_day = serializers.BooleanField(default=True)

    def create(self, validated_data):
        self.user = validated_data['user']
        self.calories = validated_data['calories']
        self.text = validated_data['text']
        self.date = validated_data['date']
        self.time = validated_data['time']
        self.less_than_calories_per_day = True
        tracker_obj = TrackerEntry.objects.create(user=self.user, calories=self.calories, text=self.text, date=self.date, time=self.time, less_than_calories_per_day=self.less_than_calories_per_day)
        return tracker_obj

    class Meta:
        model = TrackerEntry
        fields = ('id', 'user', 'calories', 'text', 'date', 'time', 'less_than_calories_per_day')