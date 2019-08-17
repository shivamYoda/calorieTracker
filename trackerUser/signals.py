from django.db.models.signals import post_save
from .models import TrackerUser
from tracker.models import TrackerEntry
from django.db.models import Sum
from datetime import datetime

def save_tracker_user(sender, instance, **kwargs):
    user_id = instance.user
    date = datetime.date()
    q = TrackerEntry.objects.filter(user=user_id, date=date)
    sum = q.aggregate(Sum('calories'))
    if sum.get('calories__sum') is not None:
        sum = sum['calories__sum']
        if sum > instance.expected_calories_per_day:
            q.update(less_than_calories_per_day=False)
        else:
            q.update(less_than_calories_per_day=True)
    return


post_save.connect(save_tracker_user, sender=TrackerUser)
