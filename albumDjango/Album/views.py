from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status

from .serializer import AlbumSerializer
from .models import Album

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def lista_albuns(request):
    try:
        albuns = Album.objects.all()  # Buscando todos os objetos Album
        if not albuns:
            return Response("erro ao buscar Albuns", status=status.HTTP_400_BAD_REQUEST)            
        serializer = AlbumSerializer(albuns, many=True)  # Serializando os dados
        return Response(serializer.data)  # Retornando a resposta em formato JSON
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

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
    # Retornando a resposta em formato JSON
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_album(request):
    try:
        serializer = AlbumSerializer(data=request.data)
                
        if serializer.is_valid():
            serializer.save()  # Salvando os dados no banco
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Retorna o álbum criado
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna erros se houver
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['PUT'])
def update_album(request):
    try:
    
        album_id = request.query_params.get('id')

        if not album_id:
            return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

        album = get_object_or_404(Album, id=album_id)
        if not album:
            return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)
        

        # Atualização (PUT)
        if request.method == 'PUT':
            # Serializar os dados recebidos para o álbum
            serializer = AlbumSerializer(album, data=request.data)
            # Verificar se os dados são válidos
            if serializer.is_valid():
                serializer.save()  # Atualizar os dados no banco de dados
                return Response(serializer.data, status=status.HTTP_200_OK)  # Retornar os dados atualizados
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_album(request):
    try:
        album_id = request.query_params.get('id')

        if not album_id:
            return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

        album = get_object_or_404(Album, id=album_id)
        if not album:
            return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)

        album.delete()  # Excluir o álbum do banco de dados
        return Response({"album deletado com sucesso"} ,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)




