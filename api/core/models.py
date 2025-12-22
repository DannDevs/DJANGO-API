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
        return f"{self.nome}"

class Cliente(AtivoMixin):
    nome = models.CharField(max_length=90)

class Vendedor(AtivoMixin):
    nome = models.CharField(max_length=90)
     
class Movimento(models.Model):
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)


# class Venda(models.Model):
#     pass
