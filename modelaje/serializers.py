from rest_framework import serializers
from .models import AreaDecision

class AreaDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaDecision
        fields = '__all__'

    def validar_rotulo(self, valor):
        if len(valor) != 7:
            raise serializers.ValidationError("El valor debe ser un 7 caracteres")
        return valor
