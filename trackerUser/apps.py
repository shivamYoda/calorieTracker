# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.apps import AppConfig

class TrackeruserConfig(AppConfig):
    name = 'trackerUser'

    def ready(self):
        TrackerUser = self.get_model('TrackerUser')
        from .signals import save_tracker_user
        post_save.connect(save_tracker_user, sender=TrackerUser, dispatch_uid="my_unique_identifier")
