from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from calorieTracker.decorators import check_jwt, track_read_access_jwt
from django.db import transaction
from django.utils.decorators import method_decorator
from trackerUser.models import TrackerUser
from .models import TrackerEntry
from rest_framework.response import Response
from rest_framework import status
from .serializers import TrackerSerializer
import requests
from calorieTracker import settings
import json
from trackerUser.permissions import Permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TrackerFilter

@method_decorator(check_jwt, name='post')
class AddEntry(APIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client_user_id = kwargs['user_id']
        user_id = request.data.get('user_id')

        if user_id is not None and client_user_id != user_id:
            if Permissions().canCreateOtherUserTrackRecords(client_user_id) is False:
                return Response(status.HTTP_403_FORBIDDEN)
        else:
            user_id = client_user_id

        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
        except TrackerUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        calories = request.data.get('calories')

        if calories is None:
            meal = request.data.get('text')
            if meal is not None:
                calories = getCalories(meal)

        params = request.data.copy()
        params['calories'] = calories
        tracker_serializer = TrackerSerializer(data=params)

        if tracker_serializer.is_valid():
            tracker_serializer.save(user=tracker_user_obj)

            return Response({'tracker_record_id': tracker_serializer.instance.id, 'status': "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(tracker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(check_jwt, name='post')
class UpdateEntry(APIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client_user_id = kwargs['user_id']
        user_id = request.data.get('user_id')


        if user_id is not None and client_user_id != user_id:
            if Permissions().canEditOtherUserTrackRecords(client_user_id) is False:
                return Response(status.HTTP_403_FORBIDDEN)
        else:
            user_id = client_user_id

        tracker_record_id = request.data.get('record_id')
        if tracker_record_id == None:
            return Response(status.HTTP_400_BAD_REQUEST)

        try:
            tracker_instance = TrackerEntry.objects.get(id=tracker_record_id)
        except TrackerEntry.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)

        text = request.data.get('text')
        calories = request.data.get('calories')

        params = request.data.copy()
        if calories is None:
            if text is not None and tracker_instance.text != text:
                calories = getCalories(text)
                params['calories'] = calories

        tracker_serializer = TrackerSerializer(instance=tracker_instance, data=params)
        if tracker_serializer.is_valid():
            tracker_serializer.save(user=tracker_instance.user)

            return Response({'status': "success"}, status=status.HTTP_200_OK)
        else:
            return Response(tracker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(check_jwt, name='post')
class DeleteEntry(APIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client_user_id = kwargs['user_id']
        user_id = request.data.get('user_id')

        if user_id is not None and client_user_id != user_id:
            if Permissions().canDeleteOtherUserTrackRecords(client_user_id) is False:
                return Response(status.HTTP_403_FORBIDDEN)
        else:
            user_id = client_user_id

        tracker_record_id = request.data.get('record_id')
        if tracker_record_id == None:
            return Response(status.HTTP_400_BAD_REQUEST)

        TrackerEntry.objects.filter(pk=tracker_record_id).delete()
        return Response({'status': "success"}, status.HTTP_200_OK)

@method_decorator(track_read_access_jwt, name='get')
class GetEntries(generics.ListAPIView):
    queryset = TrackerEntry.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TrackerFilter
    serializer_class = TrackerSerializer

def getCalories(meal):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    payload = {'query': meal}
    headers = {'content-type': 'application/json', 'x-app-id': settings.NUTRITIONIX_KEYS['app-id'], 'x-app-key': settings.NUTRITIONIX_KEYS['app-key'], 'x-remote-user-id': '0'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    calories = None
    if response.status_code == 200:
        result = response.json()
        if result.get('foods') is not None:
            foods_list = result['foods']
            food_data = foods_list[0]
            calories = food_data['nf_calories']
            return int(calories)
    return calories

add_entry = AddEntry.as_view()
update_entry = UpdateEntry.as_view()
delete_entry = DeleteEntry.as_view()