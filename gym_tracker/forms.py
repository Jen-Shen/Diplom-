from django.forms import ModelForm
from .models import Gym, UserProfile, Workout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from datetime import date


class GymForm(ModelForm):
    title = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.HiddenInput)
    info = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Gym
        fields = ['user', 'title', 'info', 'date', 'picture']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )

    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2', ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'age', 'weight', 'height', 'activity_level', 'workouts_per_week']
        labels = {
            'gender': 'Пол',
            'age': 'Возраст',
            'weight': 'Вес',
            'height': 'Рост',
            'activity_level': 'Уровень физической активности',
            'workouts_per_week': 'Количество занятий в неделю',
        }
        widgets = {
            'gender': forms.RadioSelect(choices=UserProfile.GENDER_CHOICES),
            'activity_level': forms.Select(choices=UserProfile.ACTIVITY_CHOICES),
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WorkoutForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        workout = super(WorkoutForm, self).save(commit=False)
        workout.user = self.user
        if commit:
            workout.save()
        return workout

