from rest_framework import viewsets
from inventory.models import Product, Order
from inventory.serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at')


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-date_order_placed')
