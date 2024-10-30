from datetime import timedelta, timezone
import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Album, Faixa

class AlbumModelTestCase(TestCase):
    def test_album_creation(self):
        album = Album.objects.create(
            titulo="Álbum de Teste",
            artista="Artista de Teste",
            data_lancamento=datetime.date.today()
        )
        self.assertEqual(album.titulo, "Álbum de Teste")
        self.assertEqual(album.artista, "Artista de Teste")
        self.assertIsInstance(album.data_lancamento, datetime.date)
        self.assertEqual(str(album), "Álbum de Teste")
        
        
    def test_album_validation(self):
        with self.assertRaises(Exception):
            Album.objects.create(titulo='awdawd', artista='Artista de Teste', data_lancamento=datetime.timezone.now().date())
        with self.assertRaises(Exception):
            Album.objects.create(titulo='Título muito longo' * 10, artista='Artista de Teste', data_lancamento=datetime.timezone.now().date())
        with self.assertRaises(Exception):
            Album.objects.create(titulo='Álbum de Teste', artista='', data_lancamento=datetime.timezone.now().date())

    def test_album_querying(self):
        album1 = Album.objects.create(titulo="Álbum 1", artista="Artista A", data_lancamento=datetime.datetime(2023, 1, 1))
        album2 = Album.objects.create(titulo="Álbum 2", artista="Artista B", data_lancamento=datetime.datetime(2022, 12, 31))

        # Busca por título
        self.assertEqual(Album.objects.filter(titulo="Álbum 1").first(), album1)

        # Ordenação por data de lançamento
        albums = Album.objects.order_by('data_lancamento')
        self.assertEqual(list(albums), [album2, album1])

    def test_album_deletion(self):
        album = Album.objects.create(titulo="Álbum 1", artista="Artista A", data_lancamento=datetime.datetime(2023, 1, 1))
        faixa = Faixa.objects.create(titulo="Faixa 1", duracao=datetime.timedelta(minutes=3))
        faixa.albuns.set([album])

        album.delete()

        # Verificar se a faixa ainda existe, mas não está mais associada ao álbum
        self.assertTrue(Faixa.objects.filter(id=faixa.id).exists())

class FaixaModelTestCase(TestCase):
    def test_faixa_creation(self):
        album = Album.objects.create(
            titulo="Álbum de Teste",
            artista="Artista de Teste",
            data_lancamento=datetime.date.today()
        )
        faixa = Faixa.objects.create(
            titulo="Faixa de Teste",
            duracao=datetime.timedelta(minutes=3, seconds=45)
        )
        faixa.albuns.add(album)
        self.assertEqual(faixa.titulo, "Faixa de Teste")
        self.assertEqual(faixa.duracao, datetime.timedelta(minutes=3, seconds=45))
        self.assertIn(album, faixa.albuns.all())
        self.assertIn(faixa, album.faixas.all())
        self.assertEqual(str(faixa.titulo), "Faixa de Teste")

    def test_faixa_album_relationship(self):
        album = Album.objects.create(titulo="Álbum 1", artista="Artista A", data_lancamento=datetime.datetime(2023, 1, 1))
        faixa = Faixa.objects.create(titulo="Faixa 1", duracao=timedelta(minutes=3))
        faixa.albuns.add(album)

        # Verificar se a faixa está associada ao álbum
        self.assertIn(album, faixa.albuns.all())

        # Remover a associação
        faixa.albuns.remove(album)
        self.assertNotIn(album, faixa.albuns.all())

    def test_faixa_querying(self):
        album = Album.objects.create(titulo="Álbum 1", artista="Artista A", data_lancamento=datetime.datetime(2023, 1, 1))
        faixa1 = Faixa.objects.create(titulo="Faixa 1", duracao=timedelta(minutes=3))
        faixa2 = Faixa.objects.create(titulo="Faixa 2", duracao=timedelta(minutes=5))
        faixa1.albuns.add(album)
        faixa1.albuns.add(album)

        # Buscar faixas por título
        self.assertEqual(Faixa.objects.filter(titulo="Faixa 1").first(), faixa1)

        # Ordenar faixas por duração
        faixas = Faixa.objects.order_by('duracao')
        self.assertEqual(list(faixas), [faixa1, faixa2])

    def test_faixa_deletion(self):
        album = Album.objects.create(titulo="Álbum 1", artista="Artista A", data_lancamento=datetime.datetime(2023, 1, 1))
        faixa = Faixa.objects.create(titulo="Faixa para Excluir", duracao=timedelta(minutes=3))
        faixa.albuns.add(album)

        faixa.delete()

        # Verificar se a faixa foi deletada
        self.assertFalse(Faixa.objects.filter(id=faixa.id).exists())
