from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status

from .serializer import AlbumSerializer
from .models import Album

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def lista_albuns(request):
    albuns = Album.objects.all()  # Buscando todos os objetos Album
    serializer = AlbumSerializer(albuns, many=True)  # Serializando os dados
    return Response(serializer.data)  # Retornando a resposta em formato JSON


@api_view(['GET'])
def get_album(request):
    
    album_id = request.query_params.get('id')

    if not album_id:
        return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_400_BAD_REQUEST)

    album = get_object_or_404(Album, id=album_id)
    
    serializer = AlbumSerializer(album)
    
    return Response(serializer.data)  # Retornando a resposta em formato JSON

@api_view(['POST'])
def create_album(request):
    
    serializer = AlbumSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()  # Salvando os dados no banco
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Retorna o álbum criado
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna erros se houver

@api_view(['PUT'])
def update_album(request):
    
    album_id = request.query_params.get('id')

    if not album_id:
        return Response({"error": "O parâmetro 'id' é necessário."}, status=200)

    album = get_object_or_404(Album, id=album_id)

    # Atualização (PUT)
    if request.method == 'PUT':
        # Serializar os dados recebidos para o álbum
        serializer = AlbumSerializer(album, data=request.data)
        # Verificar se os dados são válidos
        if serializer.is_valid():
            serializer.save()  # Atualizar os dados no banco de dados
            return Response(serializer.data)  # Retornar os dados atualizados
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_album(request):
    
    album_id = request.query_params.get('id')

    if not album_id:
        return Response({"error": "O parâmetro 'id' é necessário."}, status=200)

    album = get_object_or_404(Album, id=album_id)

    album.delete()  # Excluir o álbum do banco de dados
    return Response(status=status.HTTP_204_NO_CONTENT)
