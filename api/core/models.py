from django.db import models

# class Usuario():
#     pass

#  --------------  CHOICES

class TipoVenda(models.TextChoices):
    ORCAMENTO = 'O','Orcamento',
    PEDIDO = 'P','Pedido'
class TipoMov(models.TextChoices):
    ENTRADA = 'E','Entrada'
    SAIDA = 'S','Saida',
    CUSTO = 'C','Custo'
class StatusVenda(models.TextChoices):
    ABERTO = 'A','Aberto',
    FATURADO = 'F','Faturado',
    CANCELADO = 'C','Cancelado'


class AtivoMixin(models.Model):

    class Status(models.TextChoices):
        ATIVO = 'A','Ativo',
        INATIVO = 'I','Inativo'

    ativo = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.ATIVO
    )
    class Meta:
        abstract = True

class Produto(AtivoMixin):
    referencia = models.CharField(max_length=10) 
    descricao = models.CharField(max_length=90)
    preco = models.DecimalField(max_digits=8,decimal_places=2)
    saldo = models.DecimalField(max_digits=7,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.id} - {self.descricao}"

class Cliente(AtivoMixin):
    nome = models.CharField(max_length=90)

class Vendedor(AtivoMixin):
    nome = models.CharField(max_length=90)
 
class Movimento(models.Model):

    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)
    tipo_mov = models.CharField(max_length=1,choices=TipoMov.choices)
    quantidade_mov = models.DecimalField(max_digits=8,decimal_places=2)
    valor_mov = models.DecimalField(max_digits=8,decimal_places=2)

class Venda(models.Model):

    status = models.CharField(max_length=1,choices=StatusVenda.choices,default=StatusVenda.ABERTO)
    tipo_venda = models.CharField(max_length=1,choices=TipoVenda.choices,default=TipoVenda.ORCAMENTO)
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.PROTECT)
    valor_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    just_cancelamento = models.CharField(max_length=200,blank=True)

class ItemVenda(models.Model):
    
    venda = models.ForeignKey(Venda,on_delete=models.CASCADE,related_name="itens")
    produto = models.ForeignKey(Produto,on_delete=models.PROTECT)
    valor_item = models.DecimalField(max_digits=8,decimal_places=2)
    quantidade_item = models.DecimalField(max_digits=8,decimal_places=2)
    sub_total = models.DecimalField(max_digits=8,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.produto.id} - {self.produto.descricao}"


class Financeiro(models.Model):

    class Pago(models.TextChoices):
        ABERTO = 'A','Aberto'
        PAGO = 'P','Pago'
        ATRASADO = 'E','Atrasado'
    
    class Tipo(models.TextChoices):
        PAGAR = 'P','Pagar'
        RECEBER = 'R','Receber'


    pago = models.CharField(max_length=1,choices=Pago.choices,default='A')
    tipo = models.CharField(max_length=1,choices=Tipo.choices)
    venda = models.ForeignKey(Venda,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10,decimal_places=2)


# class caixa_mov(models.Model):
# 




    
    
