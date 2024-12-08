from rest_framework import serializers
from .models import AreaDecision, OpcionDecision, AreaComparacion

class AreaDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    rotulo = serializers.CharField()
    area = serializers.CharField(source='title')  # Maps `title` to `area`
    description = serializers.CharField()
    is_important = serializers.BooleanField(required=False, default=False)
    opciones = serializers.SerializerMethodField()

    class Meta:
        model = AreaDecision
        fields = ['id', 'rotulo', 'area', 'description', 'is_important', 'opciones']

    def validar_rotulo(self, valor):
        if len(valor) != 7:
            raise serializers.ValidationError("El valor debe ser un 7 caracteres")
        return valor

    def create(self, validated_data):
        # Map the `title` field from `area`
        title = validated_data.pop('title')
        validated_data['title'] = title

        # Create the AreaDecision instance
        return AreaDecision.objects.create(**validated_data)

    def get_opciones(self, obj):
        opciones = obj.opciondecision_set.all()
        return OpcionDecisionSerializer(opciones, many=True).data

class OpcionDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    descripcion = serializers.CharField(source='description')  # Maps `description` to `descripcion`
    cod_area = serializers.ReadOnlyField(source='area_decision.id')  # Read-only, derived from AreaDecision

    class Meta:
        model = OpcionDecision
        fields = ['id', 'descripcion', 'cod_area']

    def create(self, validated_data):
        # Map 'descripcion' back to 'description'
        description = validated_data.pop('description')
        area_decision = validated_data.get('area_decision')

        return OpcionDecision.objects.create(description=description, area_decision=area_decision)

class AreaComparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaComparacion
        fields = ['id', 'rotulo', 'title', 'order']