from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from .models import AreaDecision, OpcionDecision, AreaComparacion
from .serializers import AreaDecisionSerializer, OpcionDecisionSerializer, AreaComparacionSerializer


@api_view(['GET'])
def get_areas(request):
    areas = AreaDecision.objects.all()
    serializer = AreaDecisionSerializer(areas, many=True)
    return Response(serializer.data)

def get_important_areas(request):
    areas = AreaComparacion.objects.filter(is_important=True)
    serializer = AreaComparacionSerializer(areas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_area(request, pk):
    try:
        area = AreaDecision.objects.get(pk=pk)
    except AreaDecision.DoesNotExist:
        return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AreaDecisionSerializer(area)
    return Response(serializer.data)

@api_view(['POST'])
def create_area(request):
    serializer = AreaDecisionSerializer(data=request.data)
    if serializer.is_valid():
        # Save the validated data to create a model instance
        instance = serializer.save()
        return Response(AreaDecisionSerializer(instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_area(request, pk):
    area = get_object_or_404(AreaDecision, pk=pk)

    serializer = AreaDecisionSerializer(instance=area, data=request.data, partial=(request.method == 'PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_area(request, pk):
    try:
        area = AreaDecision.objects.get(pk=pk)
    except AreaDecision.DoesNotExist:
        return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)

    area.delete()
    return Response({'message': 'Area deleted successfully'}, status=status.HTTP_200_OK)

# Opciones de decision

@api_view(['GET'])
def get_opciones(request):
    opciones = OpcionDecision.objects.all()
    serializer = OpcionDecisionSerializer(opciones, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_opciones_de_area(request, area_pk):
    opciones = OpcionDecision.objects.filter(area_decision=area_pk)
    serializer = OpcionDecisionSerializer(opciones, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_opcion(request):
    data = request.data.copy()
    cod_area = data.get('cod_area')
    if not cod_area:
        return Response({'error': 'cod_area is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        area_decision = AreaDecision.objects.get(id=cod_area)
    except AreaDecision.DoesNotExist:
        return Response({'error': 'AreaDecision with the given cod_area does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data['area_decision'] = area_decision.id

    serializer = OpcionDecisionSerializer(data=data)
    if serializer.is_valid():
        opcion = serializer.save(area_decision=area_decision)  # Save the linked instance
        return Response(OpcionDecisionSerializer(opcion).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_opcion(request, pk):
    opcion = get_object_or_404(OpcionDecision, pk=pk)

    serializer = OpcionDecisionSerializer(instance=opcion, data=request.data, partial=(request.method == 'PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_opcion(request, pk):
    try:
        opcion = OpcionDecision.objects.get(pk=pk)
    except OpcionDecision.DoesNotExist:
        return Response({'error': 'Option not found'}, status=status.HTTP_404_NOT_FOUND)
    opcion.delete()
    return Response({'message': 'Option deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Areas de Comparación

@api_view(['GET'])
def get_comparaciones(request):
    comparaciones = AreaComparacion.objects.all()
    serializer = AreaComparacionSerializer(comparaciones, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_comparacion(request):
    serializer = AreaComparacionSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(AreaComparacionSerializer(instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_comparacion(request, pk):
    comparacion = get_object_or_404(AreaComparacion, pk=pk)
    serializer = AreaComparacionSerializer(instance=comparacion, data=request.data, partial=(request.method == 'PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_comparacion(request, pk):
    try:
        comparacion = AreaComparacion.objects.get(pk=pk)
    except AreaComparacion.DoesNotExist:
        return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)

    comparacion.delete()
    return Response({'message': 'Area deleted successfully'},status=status.HTTP_204_NO_CONTENT)