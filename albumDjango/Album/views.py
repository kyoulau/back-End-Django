import logging
from django.http import JsonResponse
from rest_framework.views import APIView
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

logger = logging.getLogger('AlbumFaixaView: ')


@extend_schema(tags=['Album']) 
class AlbumView(APIView):
    def get(self, request):
        try:
            albuns = Album.objects.all()
            if not albuns:
                logger.debug('erro ao listar Albuns')
                return Response("erro ao buscar Albuns", status=status.HTTP_400_BAD_REQUEST)   
                        
            serializer = AlbumSerializer(albuns, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            logger.debug('erro ao listar Albuns')
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao listar Albuns.",
                    "error": str(e)
                }, status= status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            serializer = AlbumSerializer(data=request.data)
                    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.debug('erro ao criar Albuns')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        except:
            logger.debug('erro ao criar Albuns')
            return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Album'])
class AlbumViewId(APIView):
    def get(self, request, id):
        try:
            if id:
                album = get_object_or_404(Album, id=id)
                if not album:
                    logger.debug('erro ao buscar Albuns')
                    return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = AlbumSerializer(album)
                return Response(serializer.data) 
        except:
            
            logger.debug('erro ao buscar Albuns')
            return Response(status=status.HTTP_400_BAD_REQUEST)
 
    def put(self, request, id):
        try:
            if not id:
                logger.debug('erro: o parâmetro id é necessario')
                return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

            album = get_object_or_404(Album, id=id)
            if not album:
                logger.debug('erro ao encontrar Album')
                return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)

            if request.method == 'PUT':
                serializer = AlbumSerializer(album, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.debug('erro ao editar Albuns')
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            if not id:
                logger.debug('erro: o parametro id é necessário')
                return Response({"error": "O parâmetro 'id' é necessário."}, status=status.HTTP_404_NOT_FOUND)

            album = get_object_or_404(Album, id=id)
            if not album:
                logger.debug('erro ao encontrar Album')
                return Response({"error": "Erro ao buscar Album"}, status=status.HTTP_404_NOT_FOUND)

            album.delete()
            return Response({"album deletado com sucesso"} ,status=status.HTTP_200_OK)
        except:
            logger.debug('erro ao apagar Album')
            return Response(status=status.HTTP_400_BAD_REQUEST)


###############################FAIXA###########################################

@extend_schema(tags=['Faixa'])
class FaixaView(APIView):
    def get(self, request):
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
            logger.debug('erro ao listar Faixas')
            
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao retornar faixas.",
                    "error": str(e)
                }, status= status.HTTP_400_BAD_REQUEST
            )
            
    def post(self, request):
        try:
            print(request.data)
            faixa = FaixaSerializer (data = request.data)
            print(faixa.is_valid())
            if faixa.is_valid():
                faixa.save()
                return Response(
                    {
                        'status':  'Sucess',
                        'message': 'Faixa criada com sucesso!'
                    }, status=status.HTTP_200_OK
                )

            logger.debug('erro ao criar Faixa')
            return Response(
                {
                    'status':  'Error',
                    'message': 'Erro ao Criar faixa'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.debug('erro ao criar Faixa')
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao criação de faixa.",
                    "error": str(e)
                }, status= status.HTTP_400_BAD_REQUEST
            )

@extend_schema(tags=['Faixa'])
class FaixaViewId(APIView):
    def get(self, request, id=None):
        try:
            if id is None:
                logger.debug('erro: o parametro id é necessario')
                return Response(
                    {
                        'status': 'Error',
                        'message': "O parâmetro 'faixa' é obrigatório."
                    },status=status.HTTP_401_UNAUTHORIZED
                )
            
            faixa = Faixa.objects.get(pk = id)
            
            if faixa is None:
                logger.debug('erro ao buscar faixa ')
                return Response(
                    {
                        'status': 'Error',
                        'message': "erro ao buscar faixa."
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
            logger.debug('erro ao apagar faixa ')
            
            raise IDNotFoundException("A faixa com o ID especificado não existe.")            
    
        except Exception as e:
            logger.debug('erro ao buscar faixa ')
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao retornar faixas.",
                    "error": str(e)
                }, status= status.HTTP_400_BAD_REQUEST
            )
            
        
    def put(self, request, id):
        params = request.data

        try:
            faixa = Faixa.objects.get(pk = id)

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
        except Faixa.DoesNotExist:
            logger.debug('erro ao apagar faixa ')
            
            raise IDNotFoundException("A faixa com o ID especificado não existe.")
        
        except Exception as e:
            logger.debug('erro ao editar faixa ')
            
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao editar faixa.",
                    "error": str(e)
                }, status= status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            faixa = Faixa.objects.get(pk = id)
            faixa.delete()
            return Response(
                {
                    "status": "Sucess",
                    "message": "Faixa excluida com sucesso!"
                },status= status.HTTP_200_OK
            )
        except Faixa.DoesNotExist:
            logger.debug('erro ao apagar faixa ')
            
            raise IDNotFoundException("A faixa com o ID especificado não existe.")
            
        except Exception as e:
            logger.debug('erro ao apagar faixa ')
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao deletar faixa.",
                    "error": str(e)
                }, status= status.HTTP_400_BAD_REQUEST
            )
            
