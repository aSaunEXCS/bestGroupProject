from django.shortcuts import render

def homepage(request):
  return render(request, 'home.html') #Display home.html on request

def leaderboard(request):
  return render(request, 'leaderboard.html')

def about(request):
  return render(request, 'about.html')

def bike_game(request):
  return render(request, 'bike_game.html')