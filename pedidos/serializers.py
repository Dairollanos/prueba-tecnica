from rest_framework import serializers

from .models import Articulo, Pedido


class articuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'

class pedidoSerializer(serializers.ModelSerializer):
    precio_sin_impuestos = serializers.IntegerField(required=False, read_only=True)
    precio_total = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Pedido
        fields = ['numero','porcentaje_impuesto','moneda', 'articulos', 'precio_sin_impuestos', 'precio_total']
