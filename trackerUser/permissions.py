from django.contrib.auth.models import User
from .models import TrackerUser
from tracker.models import TrackerEntry

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Permissions:

    def canEditOtherUserRecords(self, user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
            if tracker_user_obj.type == 'admin' or tracker_user_obj.type == 'user_manager':
                return True
            else:
                return False

        except TrackerUser.DoesNotExist:
            return False


    def canDeleteOtherUserRecords(self, user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
            if tracker_user_obj.type == 'admin' or tracker_user_obj.type == 'user_manager':
                return True
            else:
                return False

        except TrackerUser.DoesNotExist:
            return False

    def canCreateOtherUserTrackRecords(self, user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
            if tracker_user_obj.type == 'admin':
                return True
            else:
                return False

        except TrackerUser.DoesNotExist:
            return False

    def canEditOtherUserTrackRecords(self, user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
            if tracker_user_obj.type == 'admin':
                return True
            else:
                return False

        except TrackerUser.DoesNotExist:
            return False

    def canDeleteOtherUserTrackRecords(self, user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
            if tracker_user_obj.type == 'admin':
                return True
            else:
                return False

        except TrackerUser.DoesNotExist:
            return False



    def  canReadRecordWithId(self, user_id, record_id):
        try:
            tracker_obj = TrackerEntry.objects.get(pk=record_id)
        except TrackerEntry.DoesNotExist:
            return False

        if tracker_obj.user.user.id == int(user_id):
            return True
        else:
            try:
                tracker_user_obj = TrackerUser.objects.get(user=user_id)
            except TrackerUser.DoesNotExist:
                 return False

            if tracker_user_obj.type == "admin":
                return True
            else:
                return False


    def canReadRecordsOfUser(self, user_id, query_user_id):

        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
        except TrackerUser.DoesNotExist:
             return False

        if tracker_user_obj.id == int(query_user_id):
            return True

        if tracker_user_obj.type == 'admin':
            return True
        else:
            return False

    def hasAccessToReadAllRecords(self, user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
        except TrackerUser.DoesNotExist:
            return False
        if tracker_user_obj.type == "admin":
            return True
        else:
            return False

    def canReadUserRecords(self, user_id, query_user_id):
        try:
            tracker_user_obj = TrackerUser.objects.get(user=user_id)
        except TrackerUser.DoesNotExist:
            return False

        if tracker_user_obj.type == "admin" or tracker_user_obj.type == "user_manager":
            return True
        else:
            if user_id == query_user_id:
                return True
            else:
                return False
