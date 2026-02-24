from django.db import transaction
from rest_framework.exceptions import ValidationError
from core import models as ml
from django.shortcuts import render,get_object_or_404
from decimal import Decimal

from django.contrib.auth.models import User


class RegistroService:
    
    @transaction.atomic
    def cadastro(username,email,password):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user



class VendedorInativarService:

    @staticmethod
    @transaction.atomic
    def execute(vendedor: ml.Vendedor):
        if vendedor.ativo == ml.AtivoMixin.Status.INATIVO:
            raise ValidationError({"detail":"Vendedor já esta inativo"})
        if vendedor.ativo == ml.AtivoMixin.Status.ATIVO:
            vendedor.ativo = ml.AtivoMixin.Status.INATIVO
            vendedor.save()    
        return vendedor

class VendedorAtivarService:

    @staticmethod
    @transaction.atomic
    def execute(vendedor: ml.Vendedor):

        if vendedor.ativo == ml.AtivoMixin.Status.ATIVO:
            raise ValidationError({"detail":"Vendedor Já esta ativo"})
        
        if vendedor.ativo == ml.AtivoMixin.Status.INATIVO:
            vendedor.ativo = ml.AtivoMixin.Status.ATIVO
            vendedor.save()
        
        return vendedor


class ProdutoCadastroService:
    
    @staticmethod
    @transaction.atomic
    def cadatro(data):
        
        produto = ml.Produto.objects.create(
            **data
        )
        movimento = ml.Movimento.objects.create(
            produto=produto,
            tipo_mov=ml.TipoMov.ENTRADA,
            quantidade_mov=produto.saldo,
            valor_mov=produto.preco
        )
        return produto

class FinanceiroBaixarService:
    
    @staticmethod
    @transaction.atomic
    def execute(financeiro: ml.Financeiro,data):

        valor_pago = data["valor_pago"]
        
        if financeiro.pago == ml.Financeiro.Pago.PAGO:
            raise ValidationError({"msg":"Esse Titulo já esta em Pago"})
        
        if valor_pago > financeiro.saldo_parcela:
            raise ValidationError({"msg":f"Valor pago ${valor_pago} Maior que a parcela ${financeiro.saldo_parcela}"})

        if financeiro.saldo_parcela == 0:
            raise ValidationError({"msg":"Titulo ja está baixado"})

        if valor_pago == financeiro.saldo_parcela:
            financeiro.pago = ml.Financeiro.Pago.PAGO
            financeiro.saldo_parcela = 0
        elif valor_pago < financeiro.saldo_parcela:
            financeiro.pago = ml.Financeiro.Pago.PARCIAL
            financeiro.saldo_parcela = financeiro.saldo_parcela - valor_pago     
        
        financeiro.save()
        return financeiro

    
class FinanceiroEstornarService:
    
    @staticmethod
    @transaction.atomic
    def execute(financeiro: ml.Financeiro,data):
        if financeiro.pago == ml.Financeiro.Pago.ABERTO:
            raise ValidationError("Titulo já esta Aberto")
        financeiro.pago = ml.Financeiro.Pago.ABERTO
        financeiro.saldo_parcela = financeiro.valor_parcela
        financeiro.save()

        return financeiro

class VendaEstornarService:
    
    @staticmethod
    @transaction.atomic
    def execute(venda: ml.Venda,data):
        
        if venda.status == ml.StatusVenda.ABERTO:
            raise ValidationError("Venda já esta em Aberto")

        if venda.financeiro_set.filter(pago='P').exists():
            raise ValidationError({"detail":"Não e possivel remover a baixa da venda pois já possui financeiro baixado"})

        financas = ml.Financeiro.objects.filter(venda=venda)
        financas.delete()
        venda.status = ml.StatusVenda.ABERTO
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
        if venda.tipo_venda == ml.StatusVenda.CANCELADO:
            raise ValidationError("Não e possivel faturar uma venda cancelada")
        

        ml.Financeiro.objects.create(
                    cliente=venda.cliente,
                    vendedor=venda.vendedor,
                    venda=venda,
                    tipo='R',
                    valor_parcela=venda.valor_total
                )

        venda.status = ml.StatusVenda.FATURADO
        venda.save()       

        return venda

class ItemVendaService:
    
    @staticmethod
    @transaction.atomic
    def execute(venda: ml.Venda,data):

        produto = data["produto"]
        quantidade = data["quantidade_item"]
        valor = data["valor_item"]

        if venda.status == ml.StatusVenda.FATURADO:
            raise ValidationError({"detail":"Venda ja Faturada"})

        if produto.saldo < quantidade:
            raise ValidationError({"detail":"Saldo Insuficiente"})
        
        if venda.tipo_venda == ml.StatusVenda.CANCELADO:
            raise ValidationError("Não e possivel faturar uma venda cancelada")

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
        
        if tipo_mov == "C":
            produto.preco = valor 
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
        if venda.tipo_venda == ml.StatusVenda.CANCELADO:
            raise ValidationError("Não e possivel faturar uma venda cancelada")

        venda.tipo_venda = ml.TipoVenda.PEDIDO
        venda.save()

        return venda

class CancelarPedidoService:
    
    @staticmethod
    @transaction.atomic
    def execute(venda: ml.Venda,data):

        justificativa = data["justificativa"]

        if len(justificativa) <= 10:
            raise ValidationError("Justificativa nao pode ter menos de 10 caracteres")

        if venda.status == ml.StatusVenda.FATURADO:
            raise ValidationError("Nao e possivel cancelar uma venda Faturada")

        if venda.status == ml.StatusVenda.CANCELADO:
            raise ValidationError("Nao e possivel cancelar uma venda já cancelada")

        for i in venda.itens.all():
            
            produto = i.produto
            produto.saldo += i.quantidade_item
            produto.save()

            ml.Movimento.objects.create(
            produto=i.produto,
            tipo_mov=ml.TipoMov.ENTRADA,
            quantidade_mov=i.quantidade_item,
            valor_mov=i.valor_item
            )


        venda.status = ml.StatusVenda.CANCELADO
        venda.just_cancelamento = justificativa

        venda.save()

        return venda


class AtivarFornecedor:
    @staticmethod
    @transaction.atomic
    def ativar(fornecedor: ml.Fornecedor):
        if fornecedor.ativo == ml.AtivoMixin.Status.ATIVO:
            raise ValidationError({"msg":"Não e possivel ativar um vendedor já ativo"})
        fornecedor.ativo = ml.AtivoMixin.Status.ATIVO

        fornecedor.save()

        return fornecedor


class InativarFornecedor:
    
    @staticmethod
    @transaction.atomic
    def inativar(fornecedor: ml.Fornecedor):
        if fornecedor.ativo == ml.AtivoMixin.Status.INATIVO:
             raise ValidationError({"msg":"Não e Possivel inativar um vendedor já inativo"})
        fornecedor.ativo = ml.AtivoMixin.Status.INATIVO
        fornecedor.save()
        return fornecedor


    