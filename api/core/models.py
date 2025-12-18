from django.db import models

# Create your models here.

class Produto(models.Model):
    referencia = models.CharField(max_lenght=10) 
    descriçao = models.CharField(max_lenght=90)
    preco = models.DecimalField(max_digits=8,decimal_places=2)