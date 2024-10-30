from datetime import timedelta, timezone
import datetime
from django.test import Client, TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from ..models import Album, Faixa

class AlbumModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            'titulo': 'Test Album',
            'artista': 'Test Artist',
            'data_lancamento': '2023-10-29',
        }
    
    def test_createValidAlbum_200(self):
        response = self.client.post(
            reverse('create_album'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, 201)