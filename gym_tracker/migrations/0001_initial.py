# Generated by Django 5.0.3 on 2024-03-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('info', models.TextField()),
                ('date', models.DateField()),
                ('picture', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
