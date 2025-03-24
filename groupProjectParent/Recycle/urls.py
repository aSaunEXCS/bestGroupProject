from django.urls import path

from .views import waste_game

urlpatterns = [
 path("", waste_game, name="Recycle"),
]
