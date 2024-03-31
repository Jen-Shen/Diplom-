from django.apps import AppConfig


class GymTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gym_tracker'

    #def ready(self):
       # import gym_tracker.signals

