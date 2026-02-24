from django.db import models

# class Usuario():
#     pass

#  --------------  CHOICES

class AçoesFinancas(models.TextChoices):
    BAIXA = 'B','Baixa',
    REMBAIXA = 'R','Remocao Baixa',
    DELETE = 'D','Delete',
    ALTERACAO = 'A','Alteraçao',
    CRIACAO = 'C','Criaçao'
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
class CargosVendedor(models.TextChoices):
    VENDEDORJ = 'J','VendedorJ',
    VENDEDORS = 'S','VendedorS',
    REPRESENTANTE = 'R','Representante',
    GERENTE = 'G','Gerente'


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
    cpfcnpj = models.CharField(max_length=18,default=0)

class Vendedor(AtivoMixin):
    nome = models.CharField(max_length=90)
    email = models.CharField(max_length=90,null=True)
    cargo = models.CharField(max_length=1,choices=CargosVendedor.choices,null=True)

class Fornecedor(AtivoMixin):
    razao_social = models.CharField(max_length=120)
    email = models.CharField(max_length=90)
    cnpjcpf = models.CharField(max_length=18)    
 
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
        PARCIAL = 'C','Parcial'
        ATRASADO = 'E','Atrasado'
    
    class Tipo(models.TextChoices):
        PAGAR = 'P','Pagar'
        RECEBER = 'R','Receber'
        CREDITO = 'C','Credito'


    pago = models.CharField(max_length=1,choices=Pago.choices,default='A')
    tipo = models.CharField(max_length=1,choices=Tipo.choices)
    venda = models.ForeignKey(Venda,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.PROTECT)
    valor_parcela = models.DecimalField(max_digits=10,decimal_places=2)
    saldo_parcela = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def save(self,*args,**kwargs):
        if self.saldo_parcela is None:
            self.saldo_parcela = self.valor_parcela
        super().save(*args,**kwargs)

class Logfinancas(models.Model):


    financeiro = models.ForeignKey(Financeiro,on_delete=models.SET_NULL,null=True)
    acao = models.CharField(max_length=1,choices=AçoesFinancas.choices)
    valor_acao = models.DecimalField(max_digits=8,decimal_places=2)
    valor_total = models.DecimalField(max_digits=8,decimal_places=2) 
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']



class Entrada(models.Model):

    class StatusNota(models.TextChoices):
        PRENOTA = 'A','PreNota'
        NOTAPROCESSADA = 'P','NotaProcessada'

    tipo = models.CharField(max_length=1,choices=StatusNota.choices)
    valor_nota = models.DecimalField(max_digits=8,decimal_places=2)
    fornecedor = models.ForeignKey(Fornecedor,on_delete=models.PROTECT)
    razao_social = models.CharField(max_length=90,blank=True)
    frete = models.DecimalField(max_digits=8,decimal_places=2)

    def save(self,*args,**kwargs):
        if self.fornecedor:
            self.razao_social = self.fornecedor.razao_social

class ItensEntrada(models.Model):
    entrada =models.ForeignKey(
        Entrada,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    produto = models.ForeignKey(Produto,on_delete=models.PROTECT)
    valor_item = models.DecimalField(max_digits=8,decimal_places=2)
    descricao = models.CharField(max_length=255,blank=True)
    quantidade_item = models.DecimalField(max_digits=8,decimal_places=2)


    def save(self,*args,**kwargs):
        if self.produto:
            self.descricao = self.produto.descricao
        super.save(*args,**kwargs)





    
    
