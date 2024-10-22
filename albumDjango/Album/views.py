from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from . serializers import FaixaSerializer 
from .models import Faixa

from .exceptions import IDNotFoundException

from .validation import validate_data

from .models import Album

@api_view(["POST"])
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

@api_view(["GET"])
def get_faixa_album(request):
    try:
        faixa = Faixa.objects.all()

        faixa_serializer = FaixaSerializer(faixa, many=True)

        return Response(
            {
                'status': 'Sucess',
                'message': 'Faixas carregadas com sucesso!',
                'faixas':faixa_serializer.data
            }, status= status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao retornar faixas.",
                "error": str(e)
            }, status= status.HTTP_400_BAD_REQUEST
        )
    
@api_view(["GET"])
def get_faixa_album_by_id(request):
    params = request.data

    try:
        faixa = Faixa.objects.get(pk = params["faixa"])

        if faixa is None:
            return Response(
                {
                    'status': 'Error',
                    'message': "O parâmetro 'faixa' é obrigatório."
                },status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = FaixaSerializer(faixa)
        return Response(
            {
                'status': 'Sucess',
                'message': "Faixa encontrada com sucesso!",
                'faixa': serializer.data
            }, status=status.HTTP_200_OK
        )
    
    except Faixa.DoesNotExist:
        raise IDNotFoundException("A faixa com o ID especificado não existe.")

    except Exception as e:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao retornar faixa.",
                "error": str(e)
            }, status= status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    
@api_view(["PUT"])
@validate_data(['faixa'])
def update_faixa_album(request):

    params = request.data

    try:
        faixa = Faixa.objects.get(pk = params["faixa"])

        if "titulo" in params:
            faixa.titulo = params["titulo"]

        if "duracao" in params:
            faixa.duracao = params["duracao"]

        if "album" in params:
            faixa.albuns = Album.objects.get(pk = params["album"])

        faixa_serializer = FaixaSerializer(faixa)

        faixa.save()

        return Response(
            {
                "status": "Sucess",
                "message": "Faixa editada com sucesso!",
                "faixa": faixa_serializer.data
            },status= status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao editar faixa.",
                "error": str(e)
            }, status= status.HTTP_400_BAD_REQUEST
        )

@api_view(["DELETE"])
@validate_data(["faixa"])
def delete_faixa_album(request):
    params = request.data

    try:
        faixa = Faixa.objects.get(pk = params["faixa"])
        faixa.delete()
        return Response(
            {
                "status": "Sucess",
                "message": "Faixa excluida com sucesso!"
            },status= status.HTTP_200_OK
        )
    except Faixa.DoesNotExist:
        raise IDNotFoundException("A faixa com o ID especificado não existe.")
        
    except Exception as e:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao deletar faixa.",
                "error": str(e)
            }, status= status.HTTP_400_BAD_REQUEST
        )