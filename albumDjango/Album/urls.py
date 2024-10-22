
"""
URL configuration for albumDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('faixas/', views.create_faixa_album , name="faixa-create"),
    path("get_faixas/", views.get_faixa_album, name="faixa-get-all"),
    path("get_faixa_id/", views.get_faixa_album_by_id, name="faixa-get-by-id"),
    path("update_faixa_album/", views.update_faixa_album, name="faixa-update"),
    path("delete_faixa/", views.delete_faixa_album, name="faixa-delete"),

    path('lista_albuns/', views.lista_albuns, name='lista_albuns'),
    path('get_album/', views.get_album, name='get_album'),
    path('create_album/', views.create_album, name='create_album'),
    path('update_album/', views.update_album, name='update_album'),
    path('delete_album/', views.delete_album, name='delete_album'),
]