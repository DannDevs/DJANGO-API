import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404
from core.models import Produto,Movimento,Cliente,Vendedor,Venda,ItemVenda
# from core.serializers import ProdutoSerializer,AjusteProdutoSerializer,CadastroProdutoSerializer,MovimentoSerializer,ClienteSerializer,CadastroClienteSerializer,VendedorSerializer
from core import serializers as sz


def validadeprodutoexiste(produto_id):
    return Produto.objects.get(id=produto_id).exist()


# -------------- LISTAR PRODUTOS -------------------

class ProdutoView(APIView):
    def get(self,request):
        produtos = Produto.objects.all()
        serializer = sz.ProdutoSerializer(produtos,many=True)
        return Response(serializer.data)

# -------------- QUERY COM ID -------------

class ProdutoViewUnico(APIView):
    def get(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = sz.ProdutoSerializer(produto,many=False)
        return Response(serializer.data)
    def put(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = sz.ProdutoSerializer(produto,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = sz.ProdutoSerializer(produto,data=request.data,partial=True)
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
        serializer = sz.CadastroProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AjustarProduto(APIView):
    def patch(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = sz.AjusteProdutoSerializer(produto,data=request.data)
        if serializer.is_valid():
            produto = serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# ------------------- TABELA DE MOVIMENTOS ---------------

class VizualizarMovimento(APIView):
    def get(self,request):
        movimentos = Movimento.objects.all()
        serializer = sz.MovimentoSerializer(movimentos,many=True)
        return Response(serializer.data)

class VizualizarMovimentoDoItem(APIView):
    def get(self,request,produto_id):
        produto = get_object_or_404(Produto,id=produto_id)
        movimentositem = Movimento.objects.filter(produto=produto)
        serializer = sz.MovimentoSerializer(movimentositem,many=True)
        return Response(serializer.data)

# ----------------- CLIENTES - MOV ----------------

class ClienteView(APIView):
    def get(self,request):
        clientes = Cliente.objects.all()
        serializer = sz.ClienteSerializer(clientes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ClienteEdit(APIView):
    def get(self,request,id):
        cliente = get_object_or_404(Cliente,id=id)
        serializer = sz.ClienteSerializer(cliente)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,id):
        cliente = Cliente.objects.get(id=id).delete()
        return Response(f"Cliente {id} Deletado com sucesso",status=status.HTTP_204_NO_CONTENT)
    def put(self,request,id):
        cliente = get_object_or_404(Cliente,id=id)
        serializer = sz.ClienteSerializer(cliente,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

class CadastroCliente(APIView):
    def post(self,request):
        serializer = sz.CadastroClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# -------------- VENDEDORES --------------------------
class VendedorView(APIView):
    def get(self,request):
        vendedores = Vendedor.objects.all()
        serializer = sz.VendedorSerializer(vendedores,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class VendedorEdit(APIView):
    def get(self,request,id):
        vendedor = get_object_or_404(Vendedor,id=id)
        serializer = sz.VendedorSerializer(vendedor)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,id):
        vendedor = get_object_or_404(Vendedor,id=id).delete()
        return Response(f"Vendedor {id} deletado com sucesso",status=status.HTTP_200_OK)
class CadastroVendedor(APIView):
    def post(self,request):
        serializer = sz.VendedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# -------------- VENDA ----------------------------

class VendaView(APIView):
    def get(self,request):
        vendas = Venda.objects.all()
        serializer = sz.VendaSerializer(vendas,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class VendaViewItens(APIView):
    def get(self,request,idvenda):
        itensvenda = ItemVenda.objects.filter(venda=idvenda)
        serializer  = sz.ItemVendaSerializer(itensvenda,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class FaturarVenda(APIView):
    def patch(self,request,id):
        venda_faturar = get_object_or_404(Venda,id=id)
        serializer = sz.VendaSerializer(venda_faturar,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GerarVenda(APIView):
    def post(self,request):
        serializer = sz.VendaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GerarItemVenda(APIView):
    def post(self,request,id):
        serializer  = sz.ItemVendaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,id):
        venda = get_object_or_404(Venda,id=id)
        serializer = sz.VendaSerializer(venda)
        return Response(serializer.data,status=status.HTTP_200_OK)

