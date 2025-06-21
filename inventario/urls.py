from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_inventario, name='listar_inventario'),  # <- URL raíz
    path('crear/', views.crear_inventario, name='crear_inventario'),
    path('editar/<int:pk>/', views.editar_inventario, name='editar_inventario'),
    path('eliminar/<int:pk>/', views.eliminar_inventario, name='eliminar_inventario'),
]
