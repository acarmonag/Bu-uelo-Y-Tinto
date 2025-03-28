from rest_framework import generics
from src.view import BaseViewSet
from infrastructure.models import Order, Product, OrderStatus, OrderDetail
from .serializer import OrderSerializer, ProductSerializer, OrderStatusSerializer, OrderDetailSerializer   
from rest_framework.permissions import IsAuthenticated
from src.lib.Order.infrastructure.Django.OrderCreateRequest import OrderCreateRequest

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
    
    def create(self, request):
        create_request = OrderCreateRequest()
        return create_request.create(request)
    
class OrderStatusView(BaseViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    # permission_classes = [IsAuthenticated]

class OrderDetailView(BaseViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Opcionalmente filtrar por order_id
        """
        queryset = OrderDetail.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order_id=order_id)
        return queryset
