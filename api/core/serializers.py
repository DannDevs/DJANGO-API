from rest_framework import serializers
from .models import Produto,Movimento,Cliente,Vendedor,Venda,ItemVenda,Financeiro
from django.db import transaction
from django.shortcuts import render,get_object_or_404




# ------------ FINANCERIO SERIALIZER ---------------


class FinanceiroBaixarSerializer(serializers.Serializer):

    def validate_pago(self,value):
        if value != Financeiro.Pago.Pago:
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

class VendaRemSerializar(serializers.ModelSerializer):

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
    
    def update(self,instance,validated_data):

        if instance.financeiro_set.filter(pago='P').exists():
            raise serializers.ValidationError({"detail":"Não e possivel remover a baixa da venda pois já possui financeiro baixado"})


        if instance.status == 'F': 
            financa = get_object_or_404(Financeiro,venda=instance.id)
            financa.delete()
            instance.status = 'A'
            instance.save()

        elif instance.status == 'A':
            raise serializers.ValidationError('detail: Pedido Já esta Aberto')

        return instance

# ------------ ITENS VENDA ------------------

class ItemVendaSerializer(serializers.ModelSerializer):
    
    quantidade = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)

    class Meta:
        model = ItemVenda
        fields = ['produto','valor_item','quantidade_item','quantidade']
        
    def validate_valor_item(self,value):
        if value <= 0:
            raise serializers.ValidationError('O Valor nao pode ser menor que zero')
        return value
    def validate_quantidate_item(self,value):
        if value <= 0:
            raise serializers.ValidationError('A Quantidade nao pode ser menor que zero')
        return value    
    
    def create(self,validated_data):
        venda = self.context['venda']
        produto = validated_data['produto']
        quantidade = validated_data['quantidade_item']
        valor = validated_data['valor_item']

        if venda.status == 'F':
            raise serializers.ValidationError('detail: Pedido Já Faturado')

        if produto.saldo < quantidade:
            raise serializers.ValidationError('Saldo Do Produto Insuficiente')

        venda.valor_total += valor * quantidade
        venda.save()

        produto.saldo -= quantidade
        produto.save()
        
        item = ItemVenda.objects.create(
            venda=venda,
            **validated_data
            )

        Movimento.objects.create(
            produto=produto,
            tipo_mov='S',
            quantidade_mov=quantidade,
            valor_mov=valor
        )
        
        return item



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
    
    def update(self,instance,validated_data):

        if instance.status == 'A': 
                instance.status = 'F'
                instance.save()

                Financeiro.objects.get_or_create(
                    venda=instance,
                    defaults={
                        'cliente':instance.cliente,
                        'vendedor':instance.vendedor,
                        'venda':instance,
                        'tipo':'R',
                        'valor':instance.valor_total
                    }
                )

        elif instance.status == 'F':
            raise serializers.ValidationError('detail: Pedido Já Faturado')

        return instance

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
        fields = ['id','produto','tipo_mov','quantidade_mov','valor_mov']


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id','ativo','referencia','descricao','preco','saldo']

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

        instance.tipo_movimento = movimento.tipo_mov 
        instance.saldo_atual = instance.saldo
        instance.preco_atual = instance.preco

        return instance


    
