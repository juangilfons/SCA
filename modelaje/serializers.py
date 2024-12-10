from rest_framework import serializers
from .models import AreaDecision, OpcionDecision, AreaComparacion

class AreaDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    rotulo = serializers.CharField()
    area = serializers.CharField(source='title')
    description = serializers.CharField()
    related_areas = serializers.StringRelatedField(many=True)
    is_important = serializers.BooleanField(required=False, default=False)
    opciones = serializers.SerializerMethodField()

    class Meta:
        model = AreaDecision
        fields = ['id', 'rotulo', 'area', 'description', 'related_areas', 'is_important', 'opciones']

    def validar_rotulo(self, valor):
        if len(valor) != 7:
            raise serializers.ValidationError("El valor debe ser de 7 caracteres")
        return valor

    def create(self, validated_data):
        title = validated_data.pop('title')
        validated_data['title'] = title

        return AreaDecision.objects.create(**validated_data)

    def get_opciones(self, obj):
        opciones = obj.opciondecision_set.all()
        return OpcionDecisionSerializer(opciones, many=True).data

class OpcionDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    descripcion = serializers.CharField(source='description')
    cod_area = serializers.ReadOnlyField(source='area_decision.id')

    class Meta:
        model = OpcionDecision
        fields = ['id', 'descripcion', 'cod_area']

    def create(self, validated_data):
        description = validated_data.pop('description')
        area_decision = validated_data.get('area_decision')

        return OpcionDecision.objects.create(description=description, area_decision=area_decision)

class AreaComparacionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    label = serializers.CharField(source='rotulo')
    comparisonArea = serializers.CharField(source='title')
    order = serializers.CharField()

    class Meta:
        model = AreaComparacion
        fields = ['id', 'label', 'comparisonArea', 'order']
