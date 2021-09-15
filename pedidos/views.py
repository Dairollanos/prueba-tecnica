from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Articulo, Pedido
from .serializers import articuloSerializer, pedidoSerializer


class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = articuloSerializer

class ArticulosPedidoList(APIView):
    def get_object(self, pk):
        try:
            return Pedido.objects.get(numero=pk)
        except Pedido.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pedido = self.get_object(pk)
        serializer = pedidoSerializer(pedido)
        return Response(serializer.data['articulos'])

class PedidoListPost(ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = pedidoSerializer

    def get_queryset(self):
        queryset = Pedido.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(numero=id)
        return queryset
    
    def post(self, request, format=None):
        serializer = pedidoSerializer(data=request.data)

        if serializer.is_valid():
            validatedData = serializer.validated_data
            articulos = validatedData.get('articulos')
            impuesto = validatedData.get('porcentaje_impuesto')
            precio_sin_imp = 0
            for articulo in articulos:
                art_obj = Articulo.objects.get(identificador = articulo)
                precio_sin_imp = precio_sin_imp + art_obj.precio_sin_impuestos
            precio_con_imp = precio_sin_imp + (precio_sin_imp * (impuesto/100))
            serializer.save(precio_sin_impuestos = precio_sin_imp, precio_total= precio_con_imp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = pedidoSerializer

    def put(self, request, pk, format=None):
        pedido = self.get_object()
        serializer = pedidoSerializer(pedido, data=request.data)
        if serializer.is_valid():
            validatedData = serializer.validated_data
            articulos = validatedData.get('articulos')
            impuesto = validatedData.get('porcentaje_impuesto')
            precio_sin_imp = 0
            for articulo in articulos:
                art_obj = Articulo.objects.get(identificador = articulo)
                precio_sin_imp = precio_sin_imp + art_obj.precio_sin_impuestos
            precio_con_imp = precio_sin_imp + (precio_sin_imp * (impuesto/100))
            serializer.save(precio_sin_impuestos = precio_sin_imp, precio_total= precio_con_imp)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        pedido = self.get_object()
        serializer = pedidoSerializer(pedido, data=request.data)
        if serializer.is_valid():
            validatedData = serializer.validated_data
            articulos = validatedData.get('articulos')
            impuesto = validatedData.get('porcentaje_impuesto')
            precio_sin_imp = 0
            for articulo in articulos:
                art_obj = Articulo.objects.get(identificador = articulo)
                precio_sin_imp = precio_sin_imp + art_obj.precio_sin_impuestos
            precio_con_imp = precio_sin_imp + (precio_sin_imp * (impuesto/100))
            serializer.save(precio_sin_impuestos = precio_sin_imp, precio_total= precio_con_imp)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


