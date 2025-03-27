'''
Modelo base para la creacion de los demas modelos.
'''
from copy import deepcopy

from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict
from src.manager import CustomManager
from infrastructure.models import User

from src.middleware import current_request


class BaseModel(models.Model):
    '''
    Contiene los campos base de los demas modelos.
    '''
    log_class = None

    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha última de modificación', auto_now=True)
    created_by = models.ForeignKey(User, verbose_name='Creado por', related_name='%(app_label)s_%(class)s_created_by', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, verbose_name='Última modificación por', related_name='%(app_label)s_%(class)s_updated_by', on_delete=models.PROTECT)
    is_active = models.BooleanField('Esta activo', default=True)
    deleted = models.BooleanField('Eliminado', default=False)

    @property
    def created_by_name(self):
        return '{0} {1} ({2})'.format(self.created_by.first_name, self.created_by.last_name, self.created_by.username)
        
    @property
    def updated_by_name(self):
        return '{0} {1} ({2})'.format(self.updated_by.first_name, self.updated_by.last_name, self.updated_by.username)
        

    objects = CustomManager()

    def __init__(self, *args, **kwargs):
        '''
        Sobreescribir el método constructor para dejar una muestra del elemento
        original, y comparar después
        '''
        super().__init__(*args, **kwargs)

        # Hacer una copia del modelo para hacer una comparación de los datos antes y ahora, al momento de dejar los logs.
        self.__initial = deepcopy(self)

    def delete(self, using=None, keep_parents=False):
        '''
        Sobreescribir el método eliminar, para no eliminar físicamente de la
        base de datos, solo hacer un update.
        '''
        self.deleted = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        '''
        Sobreescribir el metodo save para colocar de forma automatica el usuario creador o el quien actualiza.
        '''
        self.change = []
        request = current_request()
        # Validar si se esta creando o editando.
        adding = self._state.adding
        if self._state.adding:
            self.created_by = request.current_request.user
            self.updated_by = request.current_request.user
        else:
            self.updated_by = request.current_request.user

        super().save(force_insert, force_update, using, update_fields)

        # Preguntar si el modelo tiene o no clase para dejar logs de cambios.
        if self.log_class and not adding:
            current = model_to_dict(self)
            initial = model_to_dict(self.__initial)

            for field in self._meta.fields:
                # Obtener el verbose_name del campo, esto para poder mostrar el log legible (en español)
                try:
                    verbose_name = field.verbose_name
                except Exception:
                    verbose_name = field.name

                #No hacer log de los campos modified_by, created_by, modified_at, created_at
                if field.name in ['modified_by', 'created_by', 'modified_at', 'created_at']:
                    continue
                if field.name not in current:
                    continue

                # Preguntar si el valor del campo cambio
                if current[field.name] != initial[field.name]:
                    before_text = None
                    after_text = None
                    before_char = None
                    after_char = None
                    if isinstance(field, models.TextField):
                        if getattr(self.__initial, field.name):
                            before_text = str(getattr(self.__initial, field.name))
                        if getattr(self, field.name):
                            after_text = str(getattr(self, field.name))
                    else:
                        if getattr(self.__initial, field.name):
                            try:
                                before_char = str(getattr(self.__initial, 'get_' + field.name + '_display')())
                            except Exception:
                                before_char = str(getattr(self.__initial, field.name))

                        if getattr(self, field.name):
                            try:
                                after_char = str(getattr(self, 'get_' + field.name + '_display')())
                            except Exception:
                                after_char = str(getattr(self, field.name))
                    
                    # Agregar el registro con el cambio a la clase de logs.
                    log_class = self.log_class(field=field.name, verbose_name=verbose_name, before_text=before_text, after_text=after_text, before_char=before_char, after_char=after_char, record=self)
                    log_class.save()
                    self.change.append({'field':field.name, 'verbose_name':verbose_name, 'before_text':before_text, 'after_text':after_text, 'before_char':before_char, 'after_char':after_char, 'record':self})


    def _get_FIELD_display(self, field):
        if field.__class__.__name__ == 'MultipleChoiceField':
            value = getattr(self, field.attname)
            choices_dict = dict(field.flatchoices)
            return [choices_dict[i] for i in value]
        return super()._get_FIELD_display(field)

    class Meta:
        '''Definir la clase como abstracta, con el fin de evitar que se cree una tabla en la base de datos y poder permitir que las demás tablas hereden de esta.'''
        abstract = True


class BaseLogModel(models.Model):
    '''
    Clase base para todos los modelos del aplicativo
    '''
    field = models.CharField('Campo', max_length=100)
    verbose_name = models.CharField('Campo', max_length=100)
    created_at = models.DateTimeField('Fecha creación', auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name='Creado por', null=True, blank=True, related_name='%(app_label)s_%(class)s_created_by', on_delete=models.PROTECT)
    deleted = models.BooleanField('Eliminar', default=False)
    before_char = models.CharField('Texto antes', max_length=500, null=True, blank=True)
    after_char = models.CharField('Texto después', max_length=500, null=True, blank=True)
    before_text = models.TextField('Texto largo antes', null=True, blank=True)
    after_text = models.TextField('Texto largo después', null=True, blank=True)
    before_id = models.IntegerField('Id antes', null=True, blank=True)
    after_id = models.IntegerField('Id después', null=True, blank=True)
    objects = CustomManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        '''
        Sobreescribir el metodo salvar para modificar datos del registro antes
        de guardar en base de datos.
        '''
        # Pregunta si se esta creando un nuevo o registro para añadir el usuario creador.
        
        adding = self._state.adding
        if adding:
            request = current_request()
            self.created_by = request.current_request.user

        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        '''Sobreescribir el metodo eleminar, para no eliminar fisicamente de la base de datos, solo hacer un update.'''
        self.deleted = True
        self.save()

    class Meta:
        '''Definir la clase como abstracta.'''
        abstract = True