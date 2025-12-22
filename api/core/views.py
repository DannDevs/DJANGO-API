import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404
from core.models import Produto
from core.serializers import ProdutoSerializer,AjusteProdutoSerializer

# -------------- LISTAR PRODUTOS -------------------

class ProdutoView(APIView):
    def get(self,request):
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos,many=True)
        return Response(serializer.data)

# -------------- QUERY COM ID -------------

class ProdutoViewUnico(APIView):
    def get(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto,many=False)
        return Response(serializer.data)
    def put(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        produto = get_object_or_404(Produto,id=id).delete()
        return Response(f"Produto {id} deletado com sucesso",status.HTTP_204_NO_CONTENT)
        
# ------------ CADASTRO PRODUTO -------------------
class CadastroProduto(APIView):
    def post(self,request):
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AjustarProduto(APIView):
    def patch(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = AjusteProdutoSerializer(produto,data=request.data)
        if serializer.is_valid():
            produto = serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

