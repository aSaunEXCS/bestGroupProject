from django.shortcuts import render
from django.http import HttpResponse

def pageView(request):
  return HttpResponse("<h1> Welcome to the BestGroup Project! </h1>") #Header text test
