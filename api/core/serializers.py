from rest_framework import serializers
from .models import Produto,Movimento,Cliente,Vendedor,Venda,ItemVenda,Financeiro,Fornecedor,ItensEntrada,Entrada,Logfinancas
from django.db import transaction
from django.shortcuts import render,get_object_or_404

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


#  LOGIN SERILIAZER

class LoginSerialiazer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email e senha são obrigatórios")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email ou senha inválidos")

        if not user.check_password(password):
            raise serializers.ValidationError("Email ou senha inválidos")

        data = super().validate({
            'username': user.username,
            'password': password
        })

        data['email'] = user.email
        data['user_id'] = user.id

        return data

#  ------------ REGISTRO SERIALIZER --------------

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {
            'email': {'required':True}
        }

    def validate_email(self,value):
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"detail":"Email já Cadastrado"})
        if len(value) < 20:
            raise serializers.ValidationError({"detail":"Tamanho menor que 20"})
        return value
            
    def validate_password(self,value):
        if len(value) < 5:
            raise serializers.ValidationError({"detail":"Senha muito curta"})
        return value


#  ------------- Total Vendas -------------

class QuantidadeVendaSerializer(serializers.Serializer):

    total_vendas = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        fields = ['total_vendas']

    def validate_total_vendas(self,value):
        if value <= 0:
            raise serializers.ValidationError({"msg":"Nenhum Resultado Encontrado"})
        return value

# ------------ FINANCERIO SERIALIZER ---------------


class FinanceiroBaixarSerializer(serializers.Serializer):

    valor_pago = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def validate_valor_pago(self,value):
        if value <= 0:
            raise serializers.ValidationError({"msg":"Valor Pago nao pode ser menor que zero"})
        return value

    def validate_valor(self,value):
        if value < 0:
            raise serializers.ValidationError('msg: Valor nao pode ser menor que zero')
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
        fields = ['id','pago','tipo','venda','cliente','vendedor','valor_parcela','saldo_parcela']

    def validate_valor(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser menor que zero')
        return 

class LogFinancasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logfinancas
        fields = ['id','financeiro','acao','valor_acao','valor_total','data']

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


class CancelarVendaSerializer(serializers.Serializer):
    justificativa = serializers.CharField(
        min_length=10,
        required=True
        )


    # def validate_justificativaR(self,valor):
    #     if len(valor) <= 15:
    #         raise serializers.ValidationError('A justificativa deve ter mais de 15 caracteres')



class VendaSerializer(serializers.ModelSerializer):
    
    financeiro = FinanceiroSerializer(
        source='financeiro_set',
        many=True,
        read_only=True
    )
    
    itens = ItemVendaSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Venda
        fields = ['id','tipo_venda','status','cliente','vendedor','valor_total','just_cancelamento','financeiro','itens']
    
    def validate_valor_total(self,value):
        if value < 0:
            raise serializers.ValidationError('detail: Valor nao pode ser Negativo')

# ------------- VENDEDOR SERIALIZER ----------------------

class VendedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendedor
        fields = ['id','ativo','nome','email','cargo']
        extra_kwargs = {
            'email': {'required':True},
            'cargo':{'required':True},
        }

    def validate_cargo(self,value):
        if value != 'J' and value != 'S' and value != 'R' and value != 'G':
            raise serializers.ValidationError({"msg":"Escolha nao e valida! J,S,R,G"})
        return value


    def validate_nome(self,value):
        if len(value) <= 3:
            raise serializers.ValidationError("O nome deve ter mais de 3 caracteres")
        return value

# -------------- CLIENTE SERIALIZER ---------------------+

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
    class Meta:
        model = Movimento
        fields = ['id','produto','produto_nome','tipo_mov','quantidade_mov','valor_mov']

class AjusteProdutoSerializer(serializers.ModelSerializer):
    
    tipo_mov = serializers.ChoiceField(
        choices=['E','S','C'],
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


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id','ativo','razao_social','email','cnpjcpf']
    
    def validate_razao_social(self,value):
        if len(value) <= 4:
            raise serializers.ValidationError({'msg':'A Razao deve ter mais de 4 caracteres'})
        return value

