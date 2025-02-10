from rest_framework import serializers
from .models import AreaDecision, OpcionDecision, AreaComparacion, DecisionAlternative, OpcionComparacion

class AreaDecisionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    rotulo = serializers.CharField()
    area = serializers.CharField(source='title')
    description = serializers.CharField()
    related_areas = serializers.StringRelatedField(many=True, required=False)
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
    symbol = serializers.CharField()
    puntuacion_minima = serializers.IntegerField(required=False, source='min_value')

    class Meta:
        model = AreaComparacion
        fields = ['id', 'label', 'comparisonArea', 'order', 'peso', 'symbol', 'puntuacion_minima']

class DecisionAlternativeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    hexa = serializers.CharField()
    options = serializers.PrimaryKeyRelatedField(queryset=OpcionDecision.objects.all(), many=True)
    values = serializers.ReadOnlyField()

    class Meta:
        model = DecisionAlternative
        fields = ['id',  'hexa', 'options', 'values']

    def get_options(self, obj):
        options = obj.options.all()
        return OpcionDecisionSerializer(options, many=True).data

    def create(self, validated_data):
        options = validated_data.pop('options')
        decision_alternative = DecisionAlternative.objects.create(**validated_data)
        decision_alternative.options.set(options)
        return decision_alternative

class OpcionComparacionSerializer(serializers.ModelSerializer):
    opcionId = serializers.PrimaryKeyRelatedField(queryset=OpcionDecision.objects.all(), source='option')
    modeId = serializers.PrimaryKeyRelatedField(queryset=AreaComparacion.objects.all(), source='area_comparacion')
    value = serializers.IntegerField()

    class Meta:
        model = OpcionComparacion
        fields = ['opcionId', 'modeId', 'value']

    def create(self, validated_data):
        if isinstance(validated_data, list):  # Si es una lista (many=True)
            return [OpcionComparacion.objects.create(**item) for item in validated_data]
        return OpcionComparacion.objects.create(**validated_data)

    def validate(self, data):
        if OpcionComparacion.objects.filter(
                option=data['option'],
                area_comparacion=data['area_comparacion']
        ).exists():
            raise serializers.ValidationError("This combination already exists.")
        return data

