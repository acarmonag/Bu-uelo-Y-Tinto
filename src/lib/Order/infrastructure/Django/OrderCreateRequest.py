from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializer import OrderSerializer
from infrastructure.models import Order, OrderDetail, Product
from infrastructure.models.order_status import OrderStatus
from django.contrib.auth import get_user_model
from decimal import Decimal

class OrderCreateRequest(APIView):
    def create(self, request):
        try:
            order_status = OrderStatus.objects.get(id=1)
            
            # Obtener datos de la orden
            order_data = {
                'delivery_location': request.data.get('delivery_location'),
                'total': Decimal('0.00'),  # Se actualizará después
                'created_by_id': request.user.id,  # Usuario del token
                'updated_by_id': request.user.id,  # Usuario del token
                'status': order_status,
                'is_active': True,
                'customer': request.user  # Usuario del token
            }
            
            # Crear la orden
            order = Order.objects.create(**order_data)
            
            # Procesar los detalles de la orden
            order_details = request.data.get('details', [])
            total = Decimal('0.00')
            
            for detail in order_details:
                product_id = detail.get('product')
                quantity = detail.get('quantity')
                
                if not product_id or not quantity:
                    continue
                
                # Obtener el producto y su precio
                product = Product.objects.get(id=product_id)
                    
                # Crear el detalle de la orden
                order_detail = OrderDetail.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,  # Precio del producto
                    created_by_id=request.user.id,  # Usuario del token
                    updated_by_id=request.user.id  # Usuario del token
                )
                
                total += order_detail.subtotal
            
            # Actualizar el total de la orden
            order.total = total
            order.save()
            
            # Serializar la respuesta
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": "Error creating order", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
