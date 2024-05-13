from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.core.signals import request_finished
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_protect
# from .models import Member
#from tester import tester
import subprocess

visdom_init_subprocess = None


# -------3D Gan Web--------------------------------------------
def index(request):
  if request.method == 'GET':
    form = LoginForm()
    return render(request, 'index.html', {'form': form})

  elif request.method == 'POST':
    form = LoginForm(request.POST)


    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
      if user:
        login(request, user)
        messages.success(request, f'Hi {username.title()}, welcome back!')
        return redirect('dashboard')

    # form is not valid or user is not authenticated
    messages.error(request, f'Invalid username or password')
    return render(request, 'index.html', {'form': form})

# def index(request):
# template = loader.get_template('index.html')
# return HttpResponse(template.render())

def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

def trigger_generator(request):
  # Start Visdom server using subprocess
  tester()
  # Redirect to Visdom page
  return redirect('index')

def open_visdom(request):
  global visdom_init_subprocess   # Start Visdom server using subprocess



  visdom_init_subprocess = subprocess.Popen(["python", "-m", "visdom.server"])

  return redirect('http://localhost:8097')   # Redirect to Visdom page


# def open_visdom(request):
#   global visdom_init_subprocess   # Start Visdom server using subprocess
#
#   cfg = {"server": "127.0.0.1",
#          "port": 8097,
#          "base_url": "/Visdom"}
#
#   vis = visdom.Visdom('http://' + cfg["server"], port=cfg["port"], base_url=cfg["base_url"])
#
#   visdom_init_subprocess = subprocess.Popen(["python", "-m", "visdom.server"])
#
#   return redirect('http://127.0.0.1:8097/Visdom')   # Redirect to Visdom page

# @receiver(request_finished)
# def close_visdom(sender, **kwargs):
#     global visdom_init_subprocess
#     if visdom_init_subprocess:
#         visdom_init_subprocess.terminate()


def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())


# ------------ UserManagement ------------------------
def sign_up(request):
  if request.method == 'GET':
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      messages.success(request, 'You have singed up successfully.')
      login(request, user)
      return redirect('dashboard')
    else:
      return render(request, 'register.html', {'form': form})


def sign_out(request):
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
    return redirect('dashboard')
  else:
    return redirect('index')




# ------------ END ------------------------
