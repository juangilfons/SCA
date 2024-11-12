from rest_framework import viewsets
from .models import AreaDecision
from .serializers import AreaDecisionSerializer


class AreaDecisionViewSet(viewsets.ModelViewSet):
    queryset = AreaDecision.objects.all()
    serializer_class = AreaDecisionSerializer
    