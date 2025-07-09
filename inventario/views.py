from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import SGI_T_INVENTARIO as Inventario
from .forms import InventarioForm  


def listar_inventario(request):
    inventarios = Inventario.objects.all().order_by('id')
    
    # Calcular el stock total
    total_stock = inventarios.aggregate(Sum('stock'))['stock__sum'] or 0

    # Contar cuántos inventarios tienen stock bajo (< 50)
    stock_bajo = inventarios.filter(stock__lt=50).count()

    return render(request, 'inventario/listar.html', {
        'inventarios': inventarios,
        'total_stock': total_stock,
        'stock_bajo': stock_bajo,
    })

def crear_inventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_inventario')
    else:
        form = InventarioForm()
    return render(request, 'inventario/formulario.html', {'form': form, 'titulo': 'Crear inventario'})

def editar_inventario(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            return redirect('listar_inventario')
    else:
        form = InventarioForm(instance=inventario)
    return render(request, 'inventario/formulario.html', {'form': form, 'titulo': 'Editar inventario'})

def eliminar_inventario(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        return redirect('listar_inventario')
    return render(request, 'inventario/confirmar_eliminar.html', {'inventario': inventario})
