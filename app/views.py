from rest_framework import generics
from src.view import BaseViewSet
from infrastructure.models import Order, Product, OrderStatus
from .serializer import OrderSerializer, ProductSerializer, OrderStatusSerializer   
from rest_framework.permissions import IsAuthenticated
# View for Product
class ProductView(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

# View for Order
class OrderView(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    
class OrderStatusView(BaseViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    # permission_classes = [IsAuthenticated]
