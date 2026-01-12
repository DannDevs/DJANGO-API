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
        if venda.status == ml.StatusVenda.FATURADO:
            raise ValidationError("Venda já Faturada")
        if venda.tipo_venda == ml.TipoVenda.ORCAMENTO:
            raise ValidationError("Nao é Possivel Faturar um orçamento")
        

        ml.Financeiro.objects.create(
                    cliente=venda.cliente,
                    vendedor=venda.vendedor,
                    venda=venda,
                    tipo='R',
                    valor=venda.valor_total
                )


        venda.status = ml.Venda.TipoVenda.FATURADO
        venda.save()

       

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

        tipo_mov = data["tipo_mov"]
        quantidade = data["quantidade"]
        valor = data["valor"]

        if tipo_mov == "S":
            if produto.saldo < quantidade:
                raise ValidationError({"detail: Saldo Insuficiente"})
            produto.saldo -= quantidade
        if tipo_mov == "E":
            produto.saldo += quantidade
        
        produto.save()

        movimento = ml.Movimento.objects.create(
            produto=produto,
            tipo_mov=tipo_mov,
            quantidade_mov=quantidade,
            valor_mov=valor
        )

        return produto

#  GERAR PEDIDO

class GerarPedidoService:
    
    @transaction.atomic
    @staticmethod
    def execute(venda: ml.Venda):

        if venda.status == ml.StatusVenda.FATURADO:
            raise ValidationError("Não e possivel gerar o pedido de uma venda faturada")
        if venda.tipo_venda == ml.TipoVenda.PEDIDO:
            raise ValidationError("Venda já e um Pedido")
        if venda.tipo_venda == ml.TipoVenda.CANCELADO:
            raise ValidationError("Não e possivel faturar uma venda cancelada")

        print(venda.tipo_venda)

        venda.tipo_venda = ml.TipoVenda.PEDIDO
        venda.save()

        return venda