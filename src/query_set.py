from django.db.models.query import QuerySet

class CustomQuerySet(QuerySet):
    '''
    QuerySet personalizado
    '''

    def delete(self):
        '''
        Actualizar masivamente una eliminación lógica
        '''

        return self.update(deleted=True)