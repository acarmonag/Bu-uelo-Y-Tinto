from django.contrib.auth.models import AbstractUser
from django.db import models
from src.model import BaseModel
from django.utils import timezone

class Customer(BaseModel):
    """Customer model representing users in the system.
    
    This model stores customer information and inherits timestamp fields
    from BaseModel (created_at, updated_at, deleted_at).
    """
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    seat = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class User(AbstractUser):
    """User model extending Django's AbstractUser.
    
    This model adds custom fields to the default Django user model
    while maintaining all authentication functionality.
    
    Inherited fields from AbstractUser:
        username: Required. 150 characters or fewer.
        password: Required. Hash of the password.
        first_name: Optional. 150 characters or fewer.
        last_name: Optional. 150 characters or fewer.
        email: Optional by default, but we make it required and unique.
        is_staff: Boolean. Designates whether user can access admin site.
        is_active: Boolean. Designates whether user account is active.
        date_joined: DateTime. When the user account was created.
    
    Custom fields:
        phone: Contact phone number
        deleted_at: Timestamp when the user was soft-deleted
    """
    
    # Override email field to make it required and unique
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        }
    )
    
    # Custom fields
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone number",
        help_text="Contact phone number"
    )
    
    # Soft delete field
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Deleted at",
        help_text="Timestamp when the user was soft-deleted"
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        """Returns a string representation of the user."""
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Returns the user's full name or username if not set."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def soft_delete(self):
        """Soft deletes the user by setting deleted_at timestamp."""
        self.deleted_at = timezone.now()
        self.is_active = False  # Also deactivate the user
        self.save()
