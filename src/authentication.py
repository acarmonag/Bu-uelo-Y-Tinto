'''
    custom_auth by Juan David González Bedoya
'''
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from infrastructure.models import User

import requests


class CustomBackend(ModelBackend):
    '''
    Autenticación personalizada, se deben definir dos metodos por lo menos
    authenticate()
    get_user()

    Documentación oficial
    https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-authentication-backends

    Leer los siguientes títulos para entender el proceso
        - Specifying authentication backends
        - Writing an authentication backend
    '''

    def authenticate(self, request, username=None, password=None):
        '''
        Autenticar el usuario por aplicación o directorio activo.
        Se ejecuta cuando se llama el authenticate() del paquete django.contrib.auth.autehnticate
        y debe de estar configurado en el settings (lista llamada AUTHENTICATION_BACKENDS)
 
        request: objecto de la petición actual
        username: username que se envió por la petición
        password: password que se envió por la petición
        '''

        try:
            # Consultar el usuario en la aplicación solo por username
            user_exist_django = User.objects.get(username=username)
            if not user_exist_django.check_password(password):
                return None


        except User.DoesNotExist:
            # None cuando NO existe el usuario en aplicación
            return None
        except ObjectDoesNotExist:
            # None cuando no encuentra información en user
            return None
        except Exception:
            # Otra novedad
            return None
        return user_exist_django


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    """
    return {
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    }


def jwt_payload_handler(user):
    """
    Returns the payload for the JWT token.
    """
    return {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': api_settings.ACCESS_TOKEN_LIFETIME,
    }
