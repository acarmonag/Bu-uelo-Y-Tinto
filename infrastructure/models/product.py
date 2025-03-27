# Infrastructure/models.py
from django.db import models
from src.model import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name
