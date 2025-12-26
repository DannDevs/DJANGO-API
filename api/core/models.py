from django.db import models

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

    class Tipo(models.TextChoices):
        ENTRADA = 'E','Entrada'
        SAIDA = 'S','Saida'

    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)
    tipo_mov = models.CharField(max_length=1,choices=Tipo.choices)
    quantidade_mov = models.DecimalField(max_digits=8,decimal_places=2)
    valor_mov = models.DecimalField(max_digits=8,decimal_places=2)

class Venda(models.Model):

    class TipoVenda(models.TextChoices):
        ABERTO = 'A','Aberto'
        FATURADO = 'F','Faturado'

    status = models.CharField(max_length=1,choices=TipoVenda.choices,default='A')
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.PROTECT)
    valor_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto,on_delete=models.PROTECT)
    valor_item = models.DecimalField(max_digits=8,decimal_places=2)
    quantidade_item = models.DecimalField(max_digits=8,decimal_places=2)

class Financeiro(models.Model):

    class Pago(models.TextChoices):
        Aberto = 'A','Aberto'
        Pago = 'P','Pago'
        Atrasado = 'E','Atrasado'
    
    class Tipo(models.TextChoices):
        Pagar = 'P','Pagar'
        Receber = 'R','Receber'


    pago = models.CharField(max_length=1,choices=Pago.choices,default='A')
    tipo = models.CharField(max_length=1,choices=Tipo.choices)
    venda = models.ForeignKey(Venda,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10,decimal_places=2)

class caixa_mov(models.Model):
    pass




    
    
