from django.db import models

# Create your models here.

class Produto(models.Model):
    referencia = models.CharField(max_length=10) 
    descricao = models.CharField(max_length=90)
    preco = models.DecimalField(max_digits=8,decimal_places=2)
    
    def __str__(self):
        return f"{self.nome}"