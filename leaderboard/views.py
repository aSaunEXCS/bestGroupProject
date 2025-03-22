from django.shortcuts import render
from .models import leaderboard
# Create your views here.

def leaderboards(request):
  all_members = leaderboard.objects.all().order_by('-points')
  return render(request, "leaderboards.html", {'all': all_members})
