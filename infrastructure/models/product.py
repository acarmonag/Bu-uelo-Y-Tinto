# Infrastructure/models.py
from django.db import models
from src.model import BaseModel

class Product(BaseModel):
    """Product model representing items available for purchase.
    
    This model stores product information and inherits timestamp fields
    from BaseModel (created_at, updated_at, deleted_at).
    """
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    image = models.URLField(
        null=True,  # Temporal para la migración
        blank=True  # Temporal para la migración
    )
    available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return f"{self.name} (${self.price if self.price else 'No price'})"
