from rest_framework import serializers
from .models import AreaDecision, OpcionDecision

class AreaDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    rotulo = serializers.CharField()  # Maps directly
    area = serializers.CharField(source='title')  # Maps `title` to `area`
    description = serializers.CharField()  # Maps directly
    is_important = serializers.BooleanField()  # Maps directly
    opciones = serializers.SerializerMethodField()

    class Meta:
        model = AreaDecision
        fields = ['id', 'rotulo', 'area', 'description', 'is_important', 'opciones']

    def validar_rotulo(self, valor):
        if len(valor) != 7:
            raise serializers.ValidationError("El valor debe ser un 7 caracteres")
        return valor

    def get_opciones(self, obj):
        # Get all related OpcionDecision objects for the AreaDecision
        opciones = obj.opciondecision_set.all()
        return OpcionDecisionSerializer(opciones, many=True).data

class OpcionDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    descripcion = serializers.CharField(source='description')
    cod_area = serializers.ReadOnlyField(source='area_decision.id')
    class Meta:
        model = OpcionDecision
        fields = ['id', 'descripcion', 'cod_area']
