from django.db import models
from trackerUser.models import TrackerUser

# Create your models here.

class TrackerEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(TrackerUser, related_name='records', on_delete=models.CASCADE)
    calories = models.IntegerField()
    text = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    less_than_calories_per_day = models.BooleanField(default=True)

    def __str__(self):
        return self.user.user.username+"_record_"+str(self.date)+"_"+str(self.time)