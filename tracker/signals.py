from django.db.models.signals import post_save
from .models import TrackerEntry
from django.db.models import Sum


def save_tracker(sender, instance, **kwargs):
    user_id = instance.user
    date = instance.date
    q = TrackerEntry.objects.filter(user=user_id, date=date)
    sum = q.aggregate(Sum('calories'))
    sum = sum['calories__sum']
    if sum > instance.user.expected_calories_per_day:
        q.update(less_than_calories_per_day=False)
    else:
        q.update(less_than_calories_per_day=True)
    return


post_save.connect(save_tracker, sender=TrackerEntry)
