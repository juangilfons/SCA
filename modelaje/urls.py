from django.urls import path, include
from . import views

urlpatterns = [
    path('api/areas/', views.get_areas, name='get_areas'),
    path('api/area/<int:pk>/', views.get_area, name='get_area'),
    path('api/area/<int:pk>/create/', views.create_area, name='create_area'),
    path('api/area/<int:pk>/update/', views.update_area, name='update_area'),
    path('api/area/<int:pk>/delete/', views.delete_area, name='delete_area'),
]
