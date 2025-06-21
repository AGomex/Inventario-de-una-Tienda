from django import forms
from .models import Inventario

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['empleado', 'producto', 'bodega', 'tipo_inventario',
                  'rotacion_inventario', 'stock', 'fecha_entrada', 'fecha_salida']
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date'}),
        }
