"""
URL configuration for hotel_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import forms, views
from app import views
from app.views import edit_post, delete_post

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from app.forms import BootstrapAuthenticationForm

from datetime import datetime
from app import forms

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('add/', views.add, name='add'),
    path('feedback/', views.feedback, name='feedback'),
    path('contacts/', views.contacts, name='contacts'),
    path('anketa/',views.anketa_view, name='anketa'),
    path('registration/', views.registration, name='registration'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'), #Редактирвоание поста
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'), # Удаление поста
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('kino/', views.kino, name='kino'),
    path('parking/', views.parking, name='parking'),
    path('standart/', views.standart, name='standart'),
    path('login/',
        LoginView.as_view
        (
            template_name='app/login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context=
            {
                'title':'Войти',
                'year':datetime.now().year,
            },
            next_page='/'
        ),
        name='login'),
    #path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
