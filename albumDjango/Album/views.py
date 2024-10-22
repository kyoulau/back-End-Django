from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from . serializers import FaixaSerializer 
from .models import Faixa

# Create your views here.
@api_view(["POST"])
# @form_validator
def create_faixa_album(request):

    try:
        faixa = FaixaSerializer (data = request.data)

        if faixa.is_valid():
            faixa.save()
        return Response(
            {
                'status':  'Sucess',
                'message': 'Faixa criada com sucesso!'
            }, status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao criação de faixa.",
                "error": str(e)
            }, status= status.HTTP_400_BAD_REQUEST
        )
    # return JsonResponse(data)