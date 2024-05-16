from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    # UserManagement
    # path('login/', views.sign_in, name='login'), # inluded on index page
    path('register/', views.sign_up, name='register'),
    path('logout/', views.sign_out, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('trigger_generator', views.trigger_generator),
    path('open-visdom', views.open_visdom),

    # Images
    path('image_upload', views.gan_image_view, name='gan_image_view'),
    path('success', views.success, name='success'),
    path('gan_images', views.display_generated_images, name = 'display_generated_images'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)