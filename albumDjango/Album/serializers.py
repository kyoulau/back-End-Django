from rest_framework import serializers
from .models import Faixa, Album

class FaixaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Faixa
        fields = '__all__'