# Generated by Django 5.1.5 on 2025-03-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0002_alter_profile_user'),
        ('leaderboard', '0002_badge_leaderboardentry_delete_leaderboard'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Badge',
        ),
        migrations.AlterField(
            model_name='profile',
            name='badges',
            field=models.ManyToManyField(blank=True, to='leaderboard.badge'),
        ),
    ]
