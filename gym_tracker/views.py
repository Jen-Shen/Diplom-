import tempfile

from django.http import HttpResponse
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, DeleteView

from .models import Gym, Video, Workout
from .forms import GymForm, UserProfileForm, RegisterForm

from utilits.recognizer.recognizer import upload
from utilits.assistant.assistant import tell_about, tell_about_workout

from datetime import date


def home(request):
    return render(request, "gym_tacker/home.html")


def get_workout_info(user_info, workout):
    initial_data = {
        'цель': workout,
        'пол': user_info.gender,
        'возраст': user_info.age,
        'вес': user_info.weight,
        'рост': user_info.height,
        'уровень активности': user_info.activity_level,
        'количество тренировок в неделю': user_info.workouts_per_week,
    }
    return initial_data


def add_for_weight_loss(request):
    if hasattr(request.user, 'userprofile'):
        user_prof = UserProfileForm(instance=request.user.userprofile)
        workout = Workout(user=request.user,
                          name="Похудение",
                          description=tell_about_workout(get_workout_info(user_prof.instance, "похудение")),
                          date=date.today())
        workout.save()
        return redirect('training-program')
    else:
        form = UserProfileForm()
        return render(request, 'gym_tacker/profile.html', {'show_message': True, 'form': form})


def add_for_muscle_gain(request):
    if hasattr(request.user, 'userprofile'):
        user_prof = UserProfileForm(instance=request.user.userprofile)
        workout = Workout(user=request.user,
                          name="Набор мышечной массы",
                          description=tell_about_workout(get_workout_info(user_prof.instance, "Рост мышц")),
                          date=date.today())
        workout.save()
        return redirect('training-program')
    else:
        form = UserProfileForm()
        return render(request, 'gym_tacker/profile.html', {'show_message': True, 'form': form})


def workout_list(request):
    forms = Workout.objects.filter(user=request.user).order_by('date')
    return render(request, 'gym_tacker/training-program.html', {'forms': forms})


class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'gym_tacker/detail_traning.html'
    context_object_name = 'workout'


class DownloadView(View):
    def get(self, request, pk):
        workout = Workout.objects.get(id=pk)
        description = workout.description

        with tempfile.TemporaryFile() as file:
            file.write(description.encode('utf-8'))
            file.seek(0)
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=description.txt'
            return response


class WorkoutDeleteView(DeleteView):
    model = Workout
    success_url = '/training-program/'
    template_name = 'gym_tacker/gym-delete.html'


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
    else:
        if hasattr(request.user, 'userprofile'):
            form = UserProfileForm(instance=request.user.userprofile)
        else:
            form = UserProfileForm()

    return render(request, 'gym_tacker/profile.html', {'form': form})


def recognize(request):
    error = ''
    if request.method == 'POST':
        form = GymForm(request.POST, request.FILES, initial={'user': request.user})
        if form.is_valid():
            instance = form.save(commit=False)
            instance.date = date.today()
            instance.save()

            title = upload("media/images/" + str(form.cleaned_data['picture']))
            instance.title = title
            instance.info = tell_about(title)
            instance.user = request.user
            instance.save()
            return redirect('result')
        else:
            print(form.errors)
            error = 'Изображение не было загружено'
    else:
        form = GymForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'gym_tacker/recognize.html', data)


def result_view(request):
    gym = Gym.objects.filter(user=request.user).order_by('date')
    return render(request, 'gym_tacker/result.html', {'gym': gym})


def upload_image(request):
    if request.method == 'POST':
        form = GymForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = GymForm()
    return render(request, 'gym_tacker/result.html', {'form': form})


class GymDetailView(DetailView):
    model = Gym
    template_name = 'gym_tacker/detail_view.html'
    context_object_name = 'gym'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = Video.objects.filter(title=self.object.title)
        context['videos'] = videos
        context['gym'] = self.object
        return context


class GymDeleteViews(DeleteView):
    model = Gym
    success_url = '/result/'
    template_name = 'gym_tacker/gym-delete.html'


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'gym_tacker/register.html', context)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'gym_tacker/register.html', context)

    return render(request, 'gym_tacker/register.html', {})


class CustomLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            logout(request)
            return redirect('login')
        else:
            return super().dispatch(request, *args, **kwargs)
