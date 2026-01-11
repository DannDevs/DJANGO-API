from rest_framework import serializers
from .models import Produto,Movimento,Cliente,Vendedor,Venda,ItemVenda,Financeiro
from django.db import transaction
from django.shortcuts import render,get_object_or_404



# ------------ FINANCERIO SERIALIZER ---------------


class FinanceiroBaixarSerializer(serializers.Serializer):

    def validate_pago(self,value):
        if value != Financeiro.Pago.PAGO:
            raise serializers.ValidationError({"Pago":"Titulo ja está Pago"})

    def validate_valor(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser menor que zero')
        return value

class FinanceiroEstornarSerializer(serializers.Serializer):

    def validate_pago(self,value):
        if value != Financeiro.Pago.Aberto:
            raise serializers.ValidationError({"detail":"Titulo já esta em aberto"})
 

    def validate_valor(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser menor que zero')
        return value

class FinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financeiro
        fields = ['id','pago','tipo','venda','cliente','vendedor','valor']

    def validate_valor(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser menor que zero')
        return value
    
# ------------- VENDA SERIALIZER -------------------

# -------------- VENDA ------------------

class VendaEstornarSerializar(serializers.ModelSerializer):

    financeiro = FinanceiroSerializer(
        source='financeiro_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Venda
        fields = ['id','status','cliente','vendedor','valor_total','financeiro']
    
    def validade_valor_total(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser Negativo')
    
# ------------ ITENS VENDA ------------------

class ItemVendaSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = ItemVenda
        fields = ['produto','valor_item','quantidade_item','sub_total']
        read_only_fields = ['sub_total']
        
    def validate_valor_item(self,value):
        if value <= 0:
            raise serializers.ValidationError('O Valor nao pode ser menor que zero')
        return value
    def validate_quantidade_item(self,value):
        if value <= 0:
            raise serializers.ValidationError('A Quantidade nao pode ser menor que zero')
        return value    
    

class VendaSerializer(serializers.ModelSerializer):
    
    financeiro = FinanceiroSerializer(
        source='financeiro_set',
        many=True,
        read_only=True
    )
    
    itens = ItemVendaSerializer(
        source ='itemvenda_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Venda
        fields = ['id','status','cliente','vendedor','valor_total','financeiro','itens']
    
    def validate_valor_total(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser Negativo')

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

    def validate_preco(self,value):
        if value <= 0:
            raise serializers.ValidationError('Preço deve ser maior que zero')
        return value
        if saldo <= 0:
            raise serializers.ValidationError('Quantidade deve ser maior que zero')
        return saldo


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id','ativo','referencia','descricao','preco','saldo']

    def validate_preco(self,value):
        if value <= 0:
            raise serializers.ValidationError('Preço Deve ser Maior que zero')
        return value 

class MovimentoSerializer(serializers.ModelSerializer):

    produto_nome = serializers.CharField(
        source='produto.descricao',
        read_only=True
    )
    print(produto_nome)
    class Meta:
        model = Movimento
        fields = ['id','produto','produto_nome','tipo_mov','quantidade_mov','valor_mov']




class AjusteProdutoSerializer(serializers.ModelSerializer):
    
    tipo_mov = serializers.ChoiceField(
        choices=['E','S'],
        write_only=True
    )
    quantidade = serializers.DecimalField(max_digits=8,decimal_places=2,write_only=True)
    valor = serializers.DecimalField(max_digits=10,decimal_places=2,write_only=True)

    class Meta:
        model = Produto
        fields = ['tipo_mov','quantidade','valor']
    
    def validate(self,data):
        tipo_mov = data.get('tipo_mov')
        quantidade = data.get('quantidade')
        valor = data.get('valor')

        if  quantidade < 0:
            raise serializers.ValidationError({'Valor':'A Quantidade nao pode ser menor que zero'})
        if  valor < 0:
            raise serializers.ValidationError({'Valor':'O Preço nao pode ser menor que zero'})
        return data

  


    
