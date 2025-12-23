from rest_framework import serializers
from .models import Produto,Movimento,Cliente,Vendedor,Venda,ItemVenda
from django.db import transaction


# ------------- VENDA SERIALIZER -------------------


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ['id','status','cliente','vendedor','valor_total']

# ------------- VENDEDOR SERIALIZER ----------------------

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id','ativo','nome']
    def validate_nome(self,value):
        if len(value) <= 3:
            raise serializers.ValidationError("O nome deve ter mais de 3 caracteres")
        return value

# -------------- CLIENTE SERIALIZER ---------------------

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','ativo','nome']
    def validate_nome(self,value):
        if len(value) <= 3:
            raise serializers.ValidationError("O nome deve ter mais de 3 caracteres")
        return value

class CadastroClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','ativo','nome']
    def validate_nome(self,value):
        if len(value) <= 3:
            raise serializers.ValidationError("O nome deve ter mais de 3 caracteres")
        return value

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

    saldo_atual = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    preco_atual = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    tipo_movimento = serializers.CharField(read_only=True)

    class Meta:
        model = Produto
        fields = ['tipo_mov','quantidade','valor','tipo_movimento','saldo_atual','preco_atual']
    
    def validate(self,data):
        tipo_mov = data.get('tipo_mov')
        quantidade = data.get('quantidade')
        valor = data.get('valor')

        if  quantidade < 0:
            raise serializers.ValidationError({'Valor':'A Quantidade nao pode ser menor que zero'})
        if  valor < 0:
            raise serializers.ValidationError({'Valor':'O Preço tem que ser menor que zero'})
        return data

    def update(self,instance,validated_data):
        quantidade = validated_data['quantidade']
        valor = validated_data['valor']
        tipo_mov = validated_data['tipo_mov']

        if tipo_mov == 'E':
            instance.saldo += quantidade
            instance.preco += valor

        elif tipo_mov == 'S':
            instance.saldo -= quantidade
            instance.preco -= valor
            
        instance.save()

        movimento = Movimento.objects.create(
                produto=instance,
                tipo_mov=tipo_mov,
                quantidade_mov=quantidade,
                valor_mov=valor
            )

        print(instance)

        instance.tipo_movimento = movimento.tipo_mov 
        instance.saldo_atual = instance.saldo
        instance.preco_atual = instance.preco

        return instance


    
