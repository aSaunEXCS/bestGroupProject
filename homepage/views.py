from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='my-login')
def homepage(request):
  return render(request, 'home.html') #Display home.html on request

def about(request):
  return render(request, 'about.html')