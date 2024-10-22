from django.urls import path
from . import views

urlpatterns = [
    path('lista_albuns/', views.lista_albuns, name='lista_albuns'),
    path('get_album/', views.get_album, name='get_album'),
    path('create_album/', views.create_album, name='create_album'),
    path('update_album/', views.update_album, name='update_album'),
    path('delete_album/', views.delete_album, name='delete_album'),
]