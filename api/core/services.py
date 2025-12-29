from django.db import transaction
from rest_framework.exceptions import ValidationError

from core import models as ml
from django.shortcuts import render,get_object_or_404






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
        
        print(data)
        produto = data["produto"]
        quantidade = data["quantidade_item"]
        valor = data["valor_item"]

        if venda.status == ml.Venda.TipoVenda.FATURADO:
            raise ValidationError({"detail":"Venda ja Faturada"})

        if produto.saldo < quantidade:
            raise ValidationError({"detail":"Saldo Insuficiente"})

        
        venda.valor_total += valor * quantidade
        venda.save()

        produto.saldo -= quantidade
        produto.save()
        
        item = ml.ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            valor_item=valor,
            quantidade_item=quantidade
            )

        ml.Movimento.objects.create(
            produto=produto,
            tipo_mov='S',
            quantidade_mov=quantidade,
            valor_mov=valor
        )
        
        return item
