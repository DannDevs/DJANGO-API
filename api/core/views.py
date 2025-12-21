import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404
from core.models import Produto


@csrf_exempt
def produtoview(request):
    
    erros = {}

    if request.method == 'GET':
        produtos = Produto.objects.all().values(
            'id','referencia','descricao','preco'
        )
        if not produtos.exists():
            return JsonResponse({'erro': 'Produto nao encontrado'},status=404)
        return JsonResponse(list(produtos),safe=False)
    else:
        return JsonResponse({'erro':'Metodo Nao Permitido'},status=405)

        

@csrf_exempt
def cadastroproduto(request):
    erros = {}
    if request.method == 'POST':
        data = json.loads(request.body)

        if not data.get('referencia'):
            erros['referencia'] = 'Campo Obrigatorio'
        if not data.get('descricao'):
            erros['descriçao'] = 'Campo Obrigatorio'
        if not data.get('preco'):
            erros['preco'] = 'Campo obrigatorio'

        if erros:
            return JsonResponse({'erro':erros},status=400)

        produto = Produto.objects.create(
            referencia=data['referencia'],
            descricao=data['descricao'],
            preco=data['preco']
        )
        return JsonResponse({
            'id':produto.id,
            'referencia':produto.referencia,
            'descricao':produto.descricao,
            'preco':produto.preco
        },status=201)

@csrf_exempt
def editarproduto(request,id):

    if request.method == 'PUT':
        data = json.loads(request.body)
        produto = get_object_or_404(Produto,id=id)
        
        produto.referencia = data.get('referencia',produto.referencia)
        produto.descricao = data.get('descricao',produto.descricao)
        produto.preco = data.get('preco',produto.preco)
        produto.save()
        return JsonResponse({
            'id':produto.id,
            'referencia':produto.referencia,
            'descricao':produto.descricao,
            'preco':produto.preco
            })

    elif request.method == 'GET':
        produto = get_object_or_404(Produto,id=id)

        return JsonResponse({
            'id':produto.id,
            'referencia':produto.referencia,
            'descricao':produto.descricao,
            'preco':produto.preco
        },status=200)

    elif request.method == 'DELETE':
        produto = get_object_or_404(Produto,id=id).delete()

        return JsonResponse({'Sucesso':f'Produto {id} Deletado com sucesso'},status=200)
    else:
        return JsonResponse({'erro':'Metodo Nao Permitido'},status=405)

