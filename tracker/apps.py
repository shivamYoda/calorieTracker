from __future__ import unicode_literals
from django.apps import AppConfig
from django.db.models.signals import post_save


class TrackerConfig(AppConfig):
    name = 'tracker'

    def ready(self):
        TrackerEntry = self.get_model('TrackerEntry')
        from .signals import save_tracker
        post_save.connect(save_tracker, sender=TrackerEntry, dispatch_uid="my_unique_identifier")
