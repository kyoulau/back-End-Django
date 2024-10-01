from django.db import models

class Album(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    data_lancamento = models.DateField()

    def __str__(self):
        return self.titulo