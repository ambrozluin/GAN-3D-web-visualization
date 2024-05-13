from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    # path('login/', views.sign_in, name='login'),
    path('register/', views.sign_up, name='register'),
    path('logout/', views.sign_out, name='logout'),



    path('dashboard/', views.dashboard, name='dashboard'),
    path('trigger_generator', views.trigger_generator),
    path('open-visdom', views.open_visdom),

]