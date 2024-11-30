from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import AreaDecision
from .serializers import AreaDecisionSerializer

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

