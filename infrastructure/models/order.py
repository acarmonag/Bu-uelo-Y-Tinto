# Infrastructure/models.py
from django.db import models
from src.model import BaseModel
from django.conf import settings  # Para referirnos al CustomUser
from .product import Product

class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    products = models.ForeignKey(Product, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} for {self.customer.username}'
    