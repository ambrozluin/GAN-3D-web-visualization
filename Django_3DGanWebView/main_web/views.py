from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, GenerateForm
from .models import GanGeneratedModel
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.core.signals import request_finished
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_protect
from .generate import generate, render_generated
import subprocess


visdom_init_subprocess = None
global_genereted_count = 6

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
  global global_genereted_count
  if request.method == 'GET':

    # getting all generate images.
    ggm = GanGeneratedModel.objects.all()
    ggm_selected = ggm[:global_genereted_count]  # Get only the specified number of objects
    return render(request, 'dashboard.html', {'gan_images': ggm_selected, 'generated_obj_count': global_genereted_count})

def trigger_generator(request):
  global global_genereted_count
  if request.method == 'POST':
    global_genereted_count = request.POST.get('generated-obj-count')
    print(global_genereted_count)
    if global_genereted_count is not None:
      try:
        generated_obj_count = int(global_genereted_count)

        # Generate with request parameters
        status = generate(obj_count=generated_obj_count)

        # when genereted get objects
        print(status)
        if (status):
          ggm = GanGeneratedModel.objects.all()
          ggm_selected = ggm[:generated_obj_count]  # Get only the specified number of objects
          return render(request, 'dashboard.html', {'gan_images': ggm_selected, 'generated_obj_count': global_genereted_count})
      except ValueError:
        return render(request, 'dashboard.html', {'error': 'Invalid number provided.'})
    else:
      return render(request, 'dashboard.html', {'error': 'Number is required.'})
  else:
    ggm = GanGeneratedModel.objects.all()
    ggm_selected = ggm[:global_genereted_count]  # Get only the specified number of objects

    return render(request, 'dashboard.html', {'gan_images': ggm_selected, 'generated_obj_count': global_genereted_count})


def open_visdom(request):
  global visdom_init_subprocess   # Start Visdom server using subprocess
  global global_genereted_count

  visdom_init_subprocess = subprocess.Popen(["python", "-m", "visdom.server"])

  render_generated(render_count=global_genereted_count)

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
  logout(request)
  return redirect("index")
  # Redirect to a success page.


# upload images

def gan_image_view(request):

    if request.method == 'POST':
      form = GenerateForm(request.POST, request.FILES)

      if form.is_valid():
        form.save()
        return redirect('success')
    else:
      form = GenerateForm()
    return render(request, 'gan_image_form.html', {'form': form})


def success(request):
  return HttpResponse('successfully uploaded')


# for displaying images

def display_generated_images(request):
  if request.method == 'GET':

    # getting all generate images.
    ggm = GanGeneratedModel.objects.all()
    return render(request, 'display_generated_images.html', {'gan_images': ggm})


# ------------ END ------------------------
