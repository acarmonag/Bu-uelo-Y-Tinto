# app/serializers.py

from rest_framework import serializers
from infrastructure.models import Product, Order, OrderStatus
from django.contrib.auth.models import User


# Serializador para Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'
