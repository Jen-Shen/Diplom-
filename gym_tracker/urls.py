from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('recognize/', views.recognize, name='recognize'),
    path('result/', views.result_view, name='result'),
    path('result/<int:pk>', views.GymDetailView.as_view(), name='gym-detail'),
    path('result/<int:pk>/delete', views.GymDeleteViews.as_view(), name='gym-delete'),
    path('register', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gym_tacker/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('training-program/', views.workout_list, name='training-program'),
    path('add_for_weight_loss/', views.add_for_weight_loss, name='add_for_weight_loss'),
    path('add_for_muscle_gain/', views.add_for_muscle_gain, name='add_for_muscle_gain'),
    path('training-program/<int:pk>/', views.WorkoutDetailView.as_view(), name='detail_training'),
    path('training-program/<int:pk>/download', views.DownloadView.as_view(), name='download_training'),
    path('training-program/<int:pk>/delete', views.WorkoutDeleteView.as_view(), name='delete_training'),
]
