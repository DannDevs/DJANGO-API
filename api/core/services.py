from django.db import transaction
from rest_framework.exceptions import ValidationError

from core import models as ml


class FinanceiroBaixarService:
    def execute(self,financeiro: ml.Financeiro):
        if financeiro.pago == ml.Financeiro.Pago.Pago:
            raise ValidationError("Esse Titulo já esta em Pago")
        financeiro.pago = ml.Financeiro.Pago.Pago
        financeiro.save()

class FinanceiroEstornarService:
    def execute(self,financeiro: ml.Financeiro):
        if financeiro.pago == ml.Financeiro.Pago.Aberto:
            raise ValidationError("Titulo já esta Aberto")
        financeiro.pago = ml.Financeiro.Pago.Aberto
        financeiro.save()
