from django.urls import path, include
from . import views

urlpatterns = [
    path('api/areas/', views.get_areas, name='get_areas'),
    path('api/area/<int:pk>/', views.get_area, name='get_area'),
    path('api/area/create/', views.create_area, name='create_area'),
    path('api/area/<int:pk>/update/', views.update_area, name='update_area'),
    path('api/area/<int:pk>/delete/', views.delete_area, name='delete_area'),

    path('api/opciones/', views.get_opciones, name='get_opciones'),
    path('api/opciones/<int:area_pk>/', views.get_opciones_de_area, name='get_opciones_area'),
    path('api/opcion/create/', views.create_opcion, name='create_opcion'),
    path('api/opcion/<int:pk>/delete/', views.delete_opcion, name='delete_opcion'),
]
