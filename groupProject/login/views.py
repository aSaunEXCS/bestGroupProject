from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . forms import CreateUserForm,LoginForm
from django.contrib.auth.models import auth
def homepage(request):
    return render(request,'index.html')
def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
    context = {'registerform':form}

    return render(request, 'register.html',context =context)


def my_login(request):
    form = LoginForm()
    if request.method=='POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect ('dashboard')
    context = {'loginform':form}
    return render(request,'my-login.html',context)



@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'dashboard.html')
# Create your views here.

def user_logout(request):

    auth.logout(request)

    return redirect("")