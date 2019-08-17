# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .serializers import TrackerUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from calorieTracker.decorators import check_jwt
from django.contrib.auth.models import  User
from django.db import transaction
from .models import TrackerUser
from .permissions import Permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TrackerUserFilter

# Create your views here.

class CreateUser(APIView):

    @transaction.atomic
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            tracker_user = TrackerUserSerializer(data=request.data)
            if tracker_user.is_valid():
                tracker_user.save(user=user.instance)
                return Response({'user_id': tracker_user.instance.id, 'status': "success"}, status=status.HTTP_201_CREATED)
            else:
                return Response(tracker_user.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(check_jwt, name='post')
class UpdateUser(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client_user_id = kwargs['user_id']
        user_id = request.data.get('user_id')

        if user_id is not None and client_user_id != user_id:
            if Permissions().canEditOtherUserRecords(client_user_id) is False:
                return Response(status.HTTP_403_FORBIDDEN)
        else:
            user_id = client_user_id

        user_instance = User.objects.get(pk=user_id)
        serializer = UserSerializer(instance=user_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            tracker_user_instance = TrackerUser.objects.get(user=user_id)
            tracker_serializer = TrackerUserSerializer(instance=tracker_user_instance, data=request.data)

            if tracker_serializer.is_valid():
                tracker_serializer.save(user=user_instance)
                return Response({'status': "success"}, status=status.HTTP_200_OK)
            else:
                return Response(tracker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(check_jwt, name='post')
class DeleteUser(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client_user_id = kwargs['user_id']
        user_id = request.data.get('user_id')

        if user_id is not None and client_user_id != user_id:
            if Permissions().canDeleteOtherUserRecords(client_user_id) is False:
                return Response(status.HTTP_403_FORBIDDEN)
        else:
            user_id = client_user_id

        User.objects.filter(pk=user_id).delete()
        return Response({'status': "success"}, status.HTTP_200_OK)


@method_decorator(check_jwt, name='get')
class GetUser(generics.ListAPIView):
    queryset = TrackerUser.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TrackerUserFilter
    serializer_class = TrackerUserSerializer

create_user = CreateUser.as_view()
update_user = UpdateUser.as_view()
delete_user = DeleteUser.as_view()
