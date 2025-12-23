from rest_framework import serializers
from .models import Produto,Movimento
from django.db import transaction



class CadastroProdutoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Produto
        fields = ['id','ativo','referencia','descricao','preco','saldo']
        extra_kwargs = {
            'ativo':{'required':True},
            'saldo':{'required':True}
        }
    def validate_preco(self,value):
        if value <= 0:
            raise serializers.ValidationError('Preço deve ser maior que zero')
        return value
        if saldo <= 0:
            raise serializers.ValidationError('Quantidade deve ser maior que zero')
        return saldo

    def create(self,validated_data):

        with transaction.atomic():
            produto = Produto.objects.create(
                **validated_data
            )
            movimento = Movimento.objects.create(
                produto=produto,
                tipo_mov='E',
                quantidade_mov=produto.saldo,
                valor_mov = produto.preco
            )
        return produto

class MovimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimento
        fields = ['produto','tipo_mov','quantidade_mov','valor_mov']


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id','ativo','referencia','descricao','preco','saldo']
        extra_kwargs = {
            'ativo':{'required':True},
            'saldo':{'required':True}
        }

    def validate_preco(self,value):
        if value <= 0:
            raise serializers.ValidationError('Preço Deve ser Maior que zero')
        return value 

class AjusteProdutoSerializer(serializers.ModelSerializer):
    tipo_mov = serializers.ChoiceField(
        choices=['E','S'],
        write_only=True
    )
    quantidade = serializers.DecimalField(max_digits=8,decimal_places=2,write_only=True)
    valor = serializers.DecimalField(max_digits=10,decimal_places=2,write_only=True)

    saldo = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    preco = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)

    class Meta:
        model = Produto
        fields = ['quantidade','valor','tipo_mov','saldo','preco']
    
    def validate(self,data):
        tipo_mov = data.get('tipo_mov')
        quantidade = data.get('quantidade')
        valor = data.get('valor')

        if  quantidade < 0:
            raise serializers.ValidationError({'Valor':'A Quantidade nao pode ser menor que zero'})
        if  valor < 0:
            raise serializers.ValidationError({'Valor':'O Preço tem que ser maior que zero'})
        return data

    def update(self,instance,validated_data):
        quantidade = validated_data['quantidade']
        valor = validated_data['valor']
        tipo_mov = validated_data['tipo_mov']

        if tipo_mov == 'E':
            instance.saldo += valor
            instance.preco += valor
            instance.save()

            Movimento.objects.create(
                produto=instance,
                tipo_mov=tipo_mov,
                preco=instance.preco,
                valor=instance.valor
            )

            return instance
        elif tipo_mov == 'S':
            instance.saldo -= valor
            instance.preco -= valor
            instance.save()

            
            Movimento.objects.create(
                produto=instance,
                tipo_mov=tipo_mov,
                quantidade_mov=valor,
                valor_mov=instance.preco
            )

            return instance


        

#   "preco": "30.00",
#   "saldo": "97.00" 

