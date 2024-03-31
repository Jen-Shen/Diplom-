from django.contrib import admin
from .models import Gym, Video, UserProfile, Workout

# Register your models here.
admin.site.register(Gym)
admin.site.register(Video)
admin.site.register(UserProfile)
admin.site.register(Workout)