# Infrastructure/models.py
from django.db import models
from django.conf import settings
from src.model import BaseModel
from .order_status import OrderStatus
from .product import Product


class Order(BaseModel):
    """Order model representing customer orders.
    
    This model stores order information and inherits timestamp fields
    from BaseModel (created_at, updated_at, deleted_at).
    """
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    delivery_location = models.CharField(
        max_length=255,
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    
    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.get_full_name() if self.customer else 'No customer'}"


class OrderDetail(BaseModel):
    """Order detail model representing items in an order.
    
    This model stores the relationship between orders and products,
    including quantity and pricing information.
    """
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='details',
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_details',
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    quantity = models.PositiveIntegerField(
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    
    class Meta:
        db_table = 'order_details'
    
    def __str__(self):
        order_id = self.order.id if self.order else 'No order'
        product_name = self.product.name if self.product else 'No product'
        return f"{order_id} - {product_name} x{self.quantity}"
    
    def save(self, *args, **kwargs):
        """Override save to calculate subtotal before saving."""
        if self.quantity and self.unit_price:
            self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    