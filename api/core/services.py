from django.db import transaction
from rest_framework.exceptions import ValidationError

from core import models as ml
from django.shortcuts import render,get_object_or_404

from decimal import Decimal

class ProdutoCadastroService:
    @staticmethod
    @transaction.atomic
    def cadatro(data):
        
        produto = ml.Produto.objects.create(
            **data
        )
        movimento = ml.Movimento.objects.create(
            produto=produto,
            tipo_mov=ml.Movimento.Tipo.ENTRADA,
            quantidade_mov=produto.saldo,
            valor_mov=produto.preco
        )
        return produto


class FinanceiroBaixarService:
    @staticmethod
    @transaction.atomic
    def execute(financeiro: ml.Financeiro,data):
        if financeiro.pago == ml.Financeiro.Pago.PAGO:
            raise ValidationError("Esse Titulo já esta em Pago")
        financeiro.pago = ml.Financeiro.Pago.PAGO
        financeiro.save()

        return financeiro

    
class FinanceiroEstornarService:
    @staticmethod
    @transaction.atomic
    def execute(financeiro: ml.Financeiro,data):
        if financeiro.pago == ml.Financeiro.Pago.ABERTO:
            raise ValidationError("Titulo já esta Aberto")
        financeiro.pago = ml.Financeiro.Pago.ABERTO
        financeiro.save()

        return financeiro

class VendaEstornarService:
    @staticmethod
    @transaction.atomic
    def execute(venda: ml.Venda,data):
        
        if venda.status == ml.Venda.TipoVenda.ABERTO:
            raise ValidationError("Venda já esta em Aberto")

        if venda.financeiro_set.filter(pago='P').exists():
            raise ValidationError({"detail":"Não e possivel remover a baixa da venda pois já possui financeiro baixado"})

        financas = ml.Financeiro.objects.filter(venda=venda)
        financas.delete()
        venda.status = ml.Venda.TipoVenda.ABERTO
        venda.save()

        return venda

class VendaFaturarService:
    
    @staticmethod
    @transaction.atomic
    def execute(venda: ml.Venda,data):    
        if venda.status == ml.Venda.TipoVenda.FATURADO:
            raise ValidationError("Venda já Faturada")
        
        venda.status = ml.Venda.TipoVenda.FATURADO
        venda.save()

        ml.Financeiro.objects.create(
                cliente=venda.cliente,
                vendedor=venda.vendedor,
                venda=venda,
                tipo='R',
                valor=venda.valor_total
                )

        return venda

class ItemVendaService:
    @staticmethod
    @transaction.atomic
    def execute(venda: ml.Venda,data):

        produto = data["produto"]
        quantidade = data["quantidade_item"]
        valor = data["valor_item"]

        if venda.status == ml.Venda.TipoVenda.FATURADO:
            raise ValidationError({"detail":"Venda ja Faturada"})

        if produto.saldo < quantidade:
            raise ValidationError({"detail":"Saldo Insuficiente"})

        total = valor * quantidade

        venda.valor_total += total
        venda.save()

        produto.saldo -= quantidade
        produto.save()
        
        item = ml.ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            valor_item=valor,
            quantidade_item=quantidade,
            sub_total=total
            )

        ml.Movimento.objects.create(
            produto=produto,
            tipo_mov='S',
            quantidade_mov=quantidade,
            valor_mov=valor
        )
        
        return item

# ---------------- SERVICE AJUSTE PRODUTO --------

class AjusteProdutoService:
    @staticmethod
    @transaction.atomic
    def execute(produto: ml.Produto,data):

        tipo_mov = data['']

        if tipo_mov == "E":
            
        if tipo_mov == "S":
































#   def update(self,instance,validated_data):
#         quantidade = validated_data['quantidade']
#         valor = validated_data['valor']
#         tipo_mov = validated_data['tipo_mov']

#         if tipo_mov == 'E':
#             instance.saldo += quantidade
#             instance.preco += valor

#         elif tipo_mov == 'S':
#             instance.saldo -= quantidade
#             instance.preco -= valor
            
#         instance.save()

#         movimento = Movimento.objects.create(
#                 produto=instance,
#                 tipo_mov=tipo_mov,
#                 quantidade_mov=quantidade,
#                 valor_mov=valor
#             )

#         instance.tipo_movimento = movimento.tipo_mov 
#         instance.saldo_atual = instance.saldo
#         instance.preco_atual = instance.preco

#         return instance