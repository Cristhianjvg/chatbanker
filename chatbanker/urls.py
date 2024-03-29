"""
URL configuration for chatbanker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from chat import views
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import redirect

def redirect_to_index(request):
    return redirect('index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_index),  # Redirige '/' a 'index'
    path('index', views.index, name='index'),
    path('vista2', views.pdf),
    path('pdf', views.pdf_correcto),
    path('chatgeneral', views.chat_general),
    path('principal', views.principal),
    path('chatprincipal', views.chatprincipal),
    path('lista_pdf', views.lista_pdf, name='lista_pdf')
]

