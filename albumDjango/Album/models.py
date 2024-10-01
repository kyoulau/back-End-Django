from django.db import models

class Album(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    data_lancamento = models.DateField()

    def __str__(self):
        return self.titulo


class Faixa(models.Model):
    titulo = models.CharField(max_length=200)
    duracao = models.DurationField()
    albuns = models.ManyToManyField(Album, related_name='faixas')  # Relacionamento N x N com Album

    def __str__(self):
        return self.title