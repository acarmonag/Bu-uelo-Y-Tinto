'''
Validaciones de formularios
'''

from django.core.validators import RegexValidator


is_alphanumericvalidator = RegexValidator(r'^[a-zA-Z0-9]*$', message='Este campo debe ser alfanumérico.', code='Inválido')

is_numbervalidator = RegexValidator(r'^[0-9]*$', message='Este campo debe ser numérico.', code='Inválido')

is_alphavalidator = RegexValidator(r'^[a-zA-Z áéíóúÁÉÍÓÚ]+$', message='Este campo sólo permite letras.', code='Inválido')