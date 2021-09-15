from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.
class Articulo(models.Model):
    identificador = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField( max_length=250)
    unidades = models.PositiveIntegerField()
    precio_sin_impuestos = models.PositiveIntegerField()

    class Meta:
        verbose_name = ("Articulo")
        verbose_name_plural = ("Articulos")

    def __str__(self):
        return self.identificador

    

class Pedido(models.Model):
    numero = models.IntegerField(primary_key=True)
    fecha_creacion = models.TimeField(auto_now_add=True)
    precio_sin_impuestos = models.PositiveIntegerField(null=True, blank=True)
    porcentaje_impuesto = models.PositiveIntegerField()
    precio_total = models.PositiveIntegerField(null=True, blank=True)
    moneda = models.CharField(max_length=50)
    articulos = models.ManyToManyField(Articulo)
    

    class Meta:
        verbose_name = ("Pedido")
        verbose_name_plural = ("Pedidos")

    def __str__(self):
        return str(self.numero) 

