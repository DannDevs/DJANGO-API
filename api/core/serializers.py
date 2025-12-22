from rest_framework import serializers
from .models import Produto


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
    campo = serializers.ChoiceField(
        choices=['saldo','preco'],
        write_only=True
    )
    valor = serializers.DecimalField(max_digits=10,decimal_places=2,write_only=True)

    saldo = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    preco = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)

    class Meta:
        model = Produto
        fields = ['campo','valor','saldo','preco']
    
    def validate(self,data):
        campo = data.get('campo')
        valor = data.get('valor')

        if campo == 'saldo' and valor < 0:
            raise serializers.ValidationError({'Valor':'o valor nao pode ser menor que zero'})
        if  campo == 'preco' and valor < 0:
            raise serializers.ValidationError({'Valor':'O Preço tem que ser maior que zero'})
        return data
    def update(self,instance,validated_data):
        campo = validated_data['campo']
        valor = validated_data['valor']

        if campo == 'saldo':
            instance.saldo += valor
        elif campo == 'preco':
            instance.preco += valor
        
        instance.save()
        return instance

#   "preco": "30.00",
#   "saldo": "97.00" 

