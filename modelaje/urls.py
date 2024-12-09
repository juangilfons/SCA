from django.urls import path, include
from . import views

urlpatterns = [
    path('api/areas/', views.get_areas, name='get_areas'),
    path('api/areas/important/', views.get_important_areas, name='get_important_areas'),
    path('api/area/<int:pk>/', views.get_area, name='get_area'),
    path('api/area/create/', views.create_area, name='create_area'),
    path('api/area/update/<int:pk>/', views.update_area, name='update_area'),
    path('api/area/delete/<int:pk>/', views.delete_area, name='delete_area'),

    path('api/opciones/', views.get_opciones, name='get_opciones'),
    path('api/opciones/<int:area_pk>/', views.get_opciones_de_area, name='get_opciones_area'),
    path('api/opcion/create/', views.create_opcion, name='create_opcion'),
    path('api/opcion/update/<int:pk>/', views.update_opcion, name='update_opcion'),
    path('api/opcion/delete/<int:pk>/', views.delete_opcion, name='delete_opcion'),

    path('api/comparaciones/', views.get_comparaciones, name='get_comparaciones'),
    path('api/comparacion/create/', views.create_comparacion, name='create_comparacion'),
    path('api/comparacion/update/<int:pk>/', views.update_comparacion, name='update_comparacion'),
    path('api/comparacion/delete/<int:pk>/', views.delete_comparacion, name='delete_comparacion'),
]
