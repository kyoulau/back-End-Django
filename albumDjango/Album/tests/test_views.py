from datetime import timedelta, timezone
import datetime
import json
from django.test import Client, TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status

from ..serializer import AlbumSerializer
from ..serializers import FaixaSerializer
from ..models import Album, Faixa

class AlbumModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.album = Album.objects.create(
            titulo='Existing Album',
            artista='Existing Artist',
            data_lancamento='2023-01-01'
        )
        self.valid_payload = {
            'titulo': 'New Album',
            'artista': 'New Artist',
            'data_lancamento': '2023-10-29'
        }
        self.invalid_payload = {
            'titulo': '',
            'artista': '',
            'data_lancamento': ''
        }

    def test_create_valid_album(self):
        response = self.client.post(
            reverse('album'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_album(self):
        response = self.client.post(
            reverse('album'),
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_existing_album(self):
        response = self.client.get(
            reverse('album-id', kwargs={'id': self.album.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.album.titulo)

    def test_get_nonexistent_album(self):
        response = self.client.get(
            reverse('album-id', kwargs={'id': 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_existing_album(self):
        updated_data = {
            'titulo': 'Updated Album',
            'artista': 'Updated Artist',
            'data_lancamento': '2023-10-30'
        }
        response = self.client.put(
            reverse('album-id', kwargs={'id': self.album.id}),
            data=updated_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.album.refresh_from_db()
        self.assertEqual(self.album.titulo, updated_data['titulo'])

    def test_delete_existing_album(self):
        response = self.client.delete(
            reverse('album-id', kwargs={'id': self.album.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())

    def test_delete_nonexistent_album(self):
        response = self.client.delete(
            reverse('album-id', kwargs={'id': 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FaixaModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.album = Album.objects.create(
            titulo='Album with Faixas',
            artista='Artist',
            data_lancamento='2023-01-01'
        )
        self.faixa = Faixa.objects.create(
            titulo='Existing Faixa',
            duracao=timedelta(seconds=180) 
        )
        self.faixa.albuns.set([self.album])
        
        self.valid_payload = {
            'titulo': 'New Faixa',
            'albuns': [self.album.id],
            'duracao': 200
        }
        self.invalid_payload = {
            'titulo': '',
            'albuns': self.album.id,
            'duracao': ''
        }

    def test_create_valid_faixa(self):
        response = self.client.post(
            reverse('faixa'),  # Ensure this points to the correct URL for creating a Faixa
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_faixa(self):
        response = self.client.post(
            reverse('faixa'),
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_existing_faixa(self):
        response = self.client.get(
            reverse('faixa-id', kwargs={'id': self.faixa.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.faixa.titulo)

    def test_update_existing_faixa(self):
        response = self.client.put(
            reverse('faixa-id', kwargs={'id': self.faixa.id}),
            data=json.dumps({
                'titulo': 'test22e'
            }),  # Convert the dictionary to a JSON string
            content_type='application/json'  # Explicitly set content type
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_existing_faixa(self):
        response = self.client.delete(
            reverse('faixa-id', kwargs={'id': self.faixa.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Faixa.objects.filter(id=self.faixa.id).exists())
