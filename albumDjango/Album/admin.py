from django.contrib import admin

from .models import Album
from .models import Faixa
# Register your models here.

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'data_lancamento')

@admin.register(Faixa)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracao')