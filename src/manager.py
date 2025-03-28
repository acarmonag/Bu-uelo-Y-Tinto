'''
Clases base para ORM.
'''

from django.db import models
from django.db.models import Q
from src.query_set import CustomQuerySet


class CustomQuerySet(models.QuerySet):
    """Custom QuerySet that filters out soft-deleted records by default."""
    
    def delete(self):
        """Override delete to perform soft delete."""
        return self.update(is_active=False, deleted_at=models.functions.Now())


class CustomManager(models.Manager):
    '''
    Manager para los query a ejecutar.
    Todos los modelos del framework usaran este manager para hacer los query a
    la base de datos, este ajustará automáticamente los query simples con el
    valor deleted=False para evitar traer elementos eliminados.
    '''

    def get_queryset(self):
        '''
        Retorna los query con filtro deleted=False en cada query ejecutado.
        '''

        return CustomQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

    def with_deleted(self):
        """Include soft-deleted records in the queryset."""
        return CustomQuerySet(self.model, using=self._db)
    
    def only_deleted(self):
        """Only include soft-deleted records in the queryset."""
        return CustomQuerySet(self.model, using=self._db).filter(deleted_at__isnull=False)
