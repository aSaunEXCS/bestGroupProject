from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='EnergyConservationMinigame_home'),
    path('toggle/<str:device_name>/', views.toggle_device, name='toggle_device'),
    path('reset/', views.reset_game, name='reset_game'),
    path('game_over/', views.game_over, name='game_over'),
]