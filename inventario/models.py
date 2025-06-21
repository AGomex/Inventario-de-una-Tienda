from django.db import models

# Create your models here.
class Rol(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.descripcion

class Empleado(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol.descripcion}"    
    
class RotacionInventario(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion

class TipoInventario(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion

class Pais(models.Model):
    pais = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.pais

class Ciudad(models.Model):
    ciudad = models.CharField(max_length=100, unique=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ciudad}, {self.pais.pais}"   

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descripcion   
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad.ciudad}, {self.ciudad.pais.pais}"   
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    fehca_elaboracion = models.DateField()
    fecha_expiracion = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.categoria.descripcion} - {self.marca.nombre}"
    
class Bodega(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.proveedor.nombre} - {self.ubicacion} ({self.capacidad} m³)"

class Stand(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    cantidad_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.codigo} - {self.bodega.proveedor.nombre} ({self.cantidad_maxima} m³, {self.cantidad_minima} m³)"

class Inventario(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    tipo_inventario = models.ForeignKey(TipoInventario, on_delete=models.CASCADE)
    rotacion_inventario = models.ForeignKey(RotacionInventario, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_entrada = models.DateField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.bodega.proveedor.nombre} ({self.stock})"

class InventarioStand(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventario.producto.nombre} - {self.stand.codigo} ({self.cantidad})"
    
class RegistroInventario(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.inventario.producto.nombre} - {self.empleado.nombre} {self.empleado.apellido} ({self.fecha_registro})"
    

