from rest_framework import serializers
from inventory.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['order_status']
        model = Order

    def create(self, validated_data):
        return Order.objects.create_order(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update_order(instance, **validated_data)
