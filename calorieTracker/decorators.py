import jwt
from django.utils.decorators import method_decorator
from calorieTracker.settings import SECRET_KEY, SIMPLE_JWT
from trackerUser.permissions import Permissions
from rest_framework.response import Response
from rest_framework import status
from trackerUser.models import TrackerUser

def check_jwt(function):
    def check(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        r = jwt.decode(token, SECRET_KEY, SIMPLE_JWT['ALGORITHM'])
        kwargs['user_id'] = r['user_id']
        return function(request, *args, **kwargs)
    return check

def track_read_access_jwt(function):
    def check(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        r = jwt.decode(token, SECRET_KEY, SIMPLE_JWT['ALGORITHM'])
        user_id = r['user_id']
        kwargs['user_id'] = r['user_id']
        queried_user_id = request.GET.get('user')
        queried_record_id = request.GET.get('id')

        if queried_record_id is not None:
            if not Permissions().canReadRecordWithId(user_id, queried_record_id):
                return Response(status=status.HTTP_403_FORBIDDEN)
        elif queried_user_id is not None:
                if Permissions().canReadRecordsOfUser(user_id, queried_user_id) == False:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                request.GET = request.GET.copy()
                print(request.GET)
        else:
            request.GET = request.GET.copy()
            if not Permissions().hasAccessToReadAllRecords(user_id):
                try:
                    tracker_user_obj = TrackerUser.objects.get(user=user_id)
                except TrackerUser.DoesNotExist:
                    return Response(status=status.HTTP_403_FORBIDDEN)

                request.GET['user'] = str(tracker_user_obj.id)

        return function(request, *args, **kwargs)

    return check


def user_read_access_jwt(function):
    def check(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        r = jwt.decode(token, SECRET_KEY, SIMPLE_JWT['ALGORITHM'])
        kwargs['user_id'] = r['user_id']
        user_id = r['user_id']
        query_user_id = request.data.get('user_id')

        if query_user_id is not None:
            if not Permissions().canReadUserRecords(user_id, query_user_id):
                return Response(status=status.HTTP_403_FORBIDDEN)

        return function(request, *args, **kwargs)
    return check