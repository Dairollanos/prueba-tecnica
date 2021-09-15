from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"Articulo", ArticuloViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('PedidoList/', PedidoListPost.as_view()),
    path('PedidoList/articulos/<int:pk>/', ArticulosPedidoList.as_view()),    
    path('PedidoList/<int:pk>/', PedidoUpdateDelete.as_view())
]
