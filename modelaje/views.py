from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import AreaDecision, OpcionDecision
from .serializers import AreaDecisionSerializer, OpcionDecisionSerializer


@api_view(['GET'])
def get_areas(request):
    areas = AreaDecision.objects.all()
    serializer = AreaDecisionSerializer(areas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_area(request, pk):
    try:
        area = AreaDecision.objects.get(pk=pk)
    except AreaDecision.DoesNotExist:
        return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_area(request):
    serializer = AreaDecisionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_area(request, pk):
    try:
        area = AreaDecision.objects.get(pk=pk)
    except AreaDecision.DoesNotExist:
        return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AreaDecisionSerializer(area=area, data=request.data, partial=(request.method == 'PATCH'))

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
    return Response({'message': 'Area deleted successfully'},status=status.HTTP_204_NO_CONTENT)

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
    serializer = OpcionDecisionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_opcion(request, pk):
    try:
        opcion = OpcionDecision.objects.get(pk=pk)
    except OpcionDecision.DoesNotExist:
        return Response({'error': 'Option not found'}, status=status.HTTP_404_NOT_FOUND)
    opcion.delete()
    return Response({'message': 'Option deleted successfully'}, status=status.HTTP_204_NO_CONTENT)