from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import JsonResponse

from . serializers import FaixaSerializer 
from .models import Faixa
from .serializer import AlbumSerializer
from .models import Album

from .exceptions import IDNotFoundException
from .validation import validate_data

@extend_schema(methods=['GET'], tags=['Album'])   
@api_view(['GET'])
def lista_albuns(request):
    try:
        albuns = Album.objects.all()
        if not albuns:
            return Response("erro ao buscar Albuns", status=status.HTTP_400_BAD_REQUEST)            
        serializer = AlbumSerializer(albuns, many=True)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(methods=['GET'], tags=['Album'])   
@api_view(['GET'])
def get_album(request):
    try:
        album_id = request.query_params.get('id')

        if not album_id:
            return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

        album = get_object_or_404(Album, id=album_id)
        if not album:
            return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AlbumSerializer(album)
        
        return Response(serializer.data) 
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(methods=['POST'], tags=['Album'])   
@api_view(['POST'])
def create_album(request):
    try:
        serializer = AlbumSerializer(data=request.data)
                
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema(methods=['PUT'], tags=['Album'])   
@api_view(['PUT'])
def update_album(request):
    try:
    
        album_id = request.query_params.get('id')

        if not album_id:
            return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

        album = get_object_or_404(Album, id=album_id)
        if not album:
            return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            serializer = AlbumSerializer(album, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(methods=['DELETE'], tags=['Album'])   
@api_view(['DELETE'])
def delete_album(request):
    try:
        album_id = request.query_params.get('id')

        if not album_id:
            return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

        album = get_object_or_404(Album, id=album_id)
        if not album:
            return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)

        album.delete()
        return Response({"album deletado com sucesso"} ,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


###############################FAIXA###########################################


@extend_schema(methods=['POST'], tags=['Faixa'])
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

@extend_schema(methods=['GET'], tags=['Faixa'])    
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
    
@extend_schema(methods=['GET'], tags=['Faixa'])   
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

    
@extend_schema(methods=['PUT'], tags=['Faixa'])     
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

@extend_schema(methods=['DELETE'], tags=['Faixa'])   
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
        
