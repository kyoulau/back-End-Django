
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

"""
    path('album/', views.lista_albuns, name='lista_albuns'),
    path('album/<int:id>', views.get_album, name='get_album'),
    path('album/', views.create_album, name='create_album'),
    path('album/<int:id>', views.update_album, name='update_album'),
    path('album/<int:id>', views.delete_album, name='delete_album'),

"""
urlpatterns = [    
    path('album/<int:id>', views.AlbumViewId.as_view(), name='album-id'),
    path('album/', views.AlbumView.as_view(), name='album'),
    
    path("faixas/<int:id>", views.FaixaViewId.as_view(), name="faixa-id"),
    path("faixas/", views.FaixaView.as_view(), name="faixa"),
    
    
]