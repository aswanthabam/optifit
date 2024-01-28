# Generated by Django 5.0.1 on 2024-01-28 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0005_remove_workout_routine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='workouts',
        ),
        migrations.AddField(
            model_name='workout',
            name='routine',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customization.routine'),
            preserve_default=False,
        ),
    ]
