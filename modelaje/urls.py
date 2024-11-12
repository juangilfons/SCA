from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AreaDecisionViewSet

router = DefaultRouter()
router.register(r'area-decisiones', AreaDecisionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]