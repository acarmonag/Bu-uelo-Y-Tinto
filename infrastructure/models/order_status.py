from django.db import models
from src.model import BaseModel


class OrderStatus(BaseModel):
    """Order status model representing possible states of an order.
    
    This model stores order status information and inherits timestamp fields
    from BaseModel (created_at, updated_at, deleted_at).
    """
    
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        db_table = 'order_statuses'
        verbose_name_plural = 'order statuses'
    
    def __str__(self):
        return self.name 