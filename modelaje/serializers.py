from rest_framework import serializers
from .models import AreaDecision, OpcionDecision

class AreaDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    rotulo = serializers.CharField()  # Maps directly
    area = serializers.CharField(source='title')  # Maps `title` to `area`
    description = serializers.CharField()  # Maps directly
    is_important = serializers.BooleanField()  # Maps directly

    class Meta:
        model = AreaDecision
        fields = ['id', 'rotulo', 'area', 'description', 'is_important']

    def validar_rotulo(self, valor):
        if len(valor) != 7:
            raise serializers.ValidationError("El valor debe ser un 7 caracteres")
        return valor

class OpcionDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionDecision
        fields = '__all__'
