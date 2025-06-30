from django.db import models

# Create your models here.
class SGI_P_ROL(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.descripcion

class SGI_M_EMPLEADO(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.ForeignKey(SGI_P_ROL, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol.descripcion}"    
    
class SGI_P_ROTACIONINVENTARIO(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion

class SGI_P_TIPOINVENTARIO(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion

class SGI_P_PAIS(models.Model):
    pais = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.pais

class SGI_P_CIUDAD(models.Model):
    ciudad = models.CharField(max_length=100, unique=True)
    pais = models.ForeignKey(SGI_P_PAIS, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ciudad}, {self.pais.pais}"   

class SGI_P_MARCA(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class SGI_P_CATEGORIA(models.Model):
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descripcion   
    
class SGI_M_PROVEEDOR(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.ForeignKey( SGI_P_CIUDAD, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad.ciudad}, {self.ciudad.pais.pais}"   
    
class SGI_M_PRODUCTO(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(SGI_M_PROVEEDOR, on_delete=models.CASCADE)
    categoria = models.ForeignKey(SGI_P_CATEGORIA, on_delete=models.CASCADE)
    marca = models.ForeignKey(SGI_P_MARCA, on_delete=models.CASCADE)
    fehca_elaboracion = models.DateField()
    fecha_expiracion = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.categoria.descripcion} - {self.marca.nombre}"
    
class SGI_M_BODEGA(models.Model):
    proveedor = models.ForeignKey(SGI_M_PROVEEDOR, on_delete=models.CASCADE)
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.proveedor.nombre} - {self.ubicacion} ({self.capacidad} m³)"

class SGI_M_STAND(models.Model):
    bodega = models.ForeignKey(SGI_M_BODEGA, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    cantidad_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.codigo} - {self.bodega.proveedor.nombre} ({self.cantidad_maxima} m³, {self.cantidad_minima} m³)"

class SGI_T_INVENTARIO(models.Model):
    empleado = models.ForeignKey(SGI_M_EMPLEADO, on_delete=models.CASCADE)
    producto = models.ForeignKey(SGI_M_PRODUCTO, on_delete=models.CASCADE)
    bodega = models.ForeignKey(SGI_M_BODEGA, on_delete=models.CASCADE)
    tipo_inventario = models.ForeignKey(SGI_P_TIPOINVENTARIO, on_delete=models.CASCADE)
    rotacion_inventario = models.ForeignKey(SGI_P_ROTACIONINVENTARIO, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_entrada = models.DateField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.bodega.proveedor.nombre} ({self.stock})"

class SGI_T_INVENTARIOSTAND (models.Model):
    inventario = models.ForeignKey(SGI_T_INVENTARIO, on_delete=models.CASCADE)
    stand = models.ForeignKey(SGI_M_STAND, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventario.producto.nombre} - {self.stand.codigo} ({self.cantidad})"
    
class SGI_T_REGISTROINVENTARIO(models.Model):
    empleado = models.ForeignKey(SGI_M_EMPLEADO, on_delete=models.CASCADE)
    inventario = models.ForeignKey(SGI_T_INVENTARIO, on_delete=models.CASCADE)
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.inventario.producto.nombre} - {self.empleado.nombre} {self.empleado.apellido} ({self.fecha_registro})"
    

