# Generated by Django 5.0.3 on 2024-03-27 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_tracker', '0005_alter_gym_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('', ''), ('M', 'Мужской'), ('F', 'Женский')], max_length=1)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('activity_level', models.CharField(choices=[('', ''), ('sedentary', 'Сидячий образ жизни'), ('moderate', 'Умеренная активность'), ('high', 'Высокая активность')], max_length=10)),
                ('workouts_per_week', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
