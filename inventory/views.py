from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from inventory.models import Product, Order
from inventory.serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at')


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-date_order_placed')

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        Order.objects.cancel_order(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)
