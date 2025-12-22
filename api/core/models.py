from django.db import models

# Create your models here.

class Produto(models.Model):
    
    ATIVO_CHOICES = {
        ('A','Ativo'),
        ('I','Inativo'),
    }
    ativo = models.CharField(max_length=1,choices=ATIVO_CHOICES,default='A')
    referencia = models.CharField(max_length=10) 
    descricao = models.CharField(max_length=90)
    preco = models.DecimalField(max_digits=8,decimal_places=2)
    
    def __str__(self):
        return f"{self.nome}"