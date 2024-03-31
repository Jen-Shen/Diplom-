from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Gym(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    info = models.TextField()
    date = models.DateField()
    picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=100)
    url = EmbedVideoField()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    ACTIVITY_CHOICES = [
        ('sedentary', 'Сидячий образ жизни'),
        ('moderate', 'Умеренная активность'),
        ('high', 'Высокая активность'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, default='')
    age = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, blank=False, default='')
    workouts_per_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])

    def __str__(self):
        return self.user.username


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            last_workout = Workout.objects.filter(user=self.user).order_by('-number').first()
            if last_workout:
                self.number = last_workout.number + 1
        super(Workout, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Workout, self).delete(*args, **kwargs)

        remaining_workouts = Workout.objects.filter(user=self.user).order_by('number')
        for index, workout in enumerate(remaining_workouts, start=1):
            workout.number = index
            workout.save()
