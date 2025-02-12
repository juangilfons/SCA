from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.management import call_command

from django.shortcuts import get_object_or_404

from .models import AreaDecision, OpcionDecision, AreaComparacion, DecisionAlternative, OpcionComparacion
from .serializers import AreaDecisionSerializer, OpcionDecisionSerializer, AreaComparacionSerializer, DecisionAlternativeSerializer, OpcionComparacionSerializer

@api_view(['GET'])
def get_areas(request):
    areas = AreaDecision.objects.all()
    serializer = AreaDecisionSerializer(areas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_important_areas(request):
    areas = AreaDecision.objects.filter(is_important=True)
    serializer = AreaDecisionSerializer(areas, many=True)
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

@api_view(['POST', 'DELETE'])
def manage_related_area(request):
    area_id = request.data.get('area_id')
    related_area_id = request.data.get('related_area_id')

    if not area_id or not related_area_id:
        return Response({'error': 'Both area_id and related_area_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        area = get_object_or_404(AreaDecision, pk=area_id)
        related_area = get_object_or_404(AreaDecision, pk=related_area_id)
    except AreaDecision.DoesNotExist:
        return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'POST':
        area.related_areas.add(related_area)
        return Response({'message': 'Relationship created successfully.'}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        area.related_areas.remove(related_area)
        return Response({'message': 'Relationship removed successfully.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_relationships(request):
    areas = AreaDecision.objects.all()
    processed_pairs = set()
    relationships = []

    for area in areas:
        related_areas = area.related_areas.all()
        for related in related_areas:
            pair_tuple = tuple(sorted([(area.id, area.title), (related.id, related.title)]))

            if pair_tuple not in processed_pairs:
                pair_str = f"{pair_tuple[0][1]} - {pair_tuple[1][1]}"  # "area1 - area2"
                relationships.append([pair_str, pair_tuple[0][0], pair_tuple[1][0]])  # ["area1 - area2", id1, id2]
                processed_pairs.add(pair_tuple)

    return Response({"vinculos": relationships})


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
    return Response({'message': 'Area deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_alternativas(request):
    alternativas = DecisionAlternative.objects.all()
    serializer = DecisionAlternativeSerializer(alternativas, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def create_alternativa(request):
    serializer = DecisionAlternativeSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(DecisionAlternativeSerializer(instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_alternativa(request, hexa):
    hexa = '#' + hexa
    try:
        alternativa = DecisionAlternative.objects.get(hexa=hexa)
    except DecisionAlternative.DoesNotExist:
        return Response({'error': 'Alternative not found'}, status=status.HTTP_404_NOT_FOUND)

    alternativa.delete()
    return Response({'message': 'Alternative deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_opciones_comparacion(request):
    opciones_comparacion = OpcionComparacion.objects.all()
    serializer = OpcionComparacionSerializer(opciones_comparacion, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_opcion_comparacion(request):
    serializer = OpcionComparacionSerializer(data=request.data, many=True)
    if serializer.is_valid():
        cells = serializer.save()
        return Response(OpcionComparacionSerializer(cells, many=True).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def bulk_update_opciones_comparacion(request):
    updates = request.data

    if not isinstance(updates, list):
        return Response({'error': 'Request data must be a list of objects.'}, status=status.HTTP_400_BAD_REQUEST)

    errors = []
    updated_objects = []

    for update in updates:
        mode_id = update.get('modeId')
        opcion_id = update.get('opcionId')

        if not mode_id or not opcion_id:
            errors.append({'error': 'Each object must contain an "id".', 'data': update})
            continue

        try:
            opcion_comparacion = OpcionComparacion.objects.get(option_id=opcion_id, area_comparacion_id=mode_id)
        except OpcionComparacion.DoesNotExist:
            errors.append({'error': f'Object does not exist.', 'mode_id': mode_id, 'opcion_id': opcion_id})
            continue

        # Check if another entry with the same mode_id and opcion_id exists
        existing_entry = OpcionComparacion.objects.filter(
            option_id=update.get('optionId'),
            area_comparacion_id=update.get('modeId')
        ).exclude(id=opcion_comparacion.id).first()

        if existing_entry:
            errors.append({
                'error': 'This combination already exists.',
                'mode_id': mode_id,
                'opcion_id': opcion_id
            })
            continue

        # Validate and save the update
        serializer = OpcionComparacionSerializer(opcion_comparacion, data=update, partial=True)
        if serializer.is_valid():
            updated_objects.append(serializer.save())
        else:
            errors.append({'error': serializer.errors, 'mode_id': mode_id, 'opcion_id': opcion_id})

    response_data = {
        'updated': OpcionComparacionSerializer(updated_objects, many=True).data,
        'errors': errors,
    }

    return Response(response_data, status=status.HTTP_200_OK if not errors else status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def reset_database(request):
    try:
        call_command('flush', '--noinput')  # Deletes all data but keeps migrations
        return JsonResponse({'message': 'Database reset successful'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
