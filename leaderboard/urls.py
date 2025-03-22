from django.urls import path

from .views import leaderboards

urlpatterns = [
    path("leaderboard", leaderboards, name="leaderboards"),
]