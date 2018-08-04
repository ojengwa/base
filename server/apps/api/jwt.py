import uuid
from calendar import timegm
from datetime import datetime

from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings


def payload_handler(user):

    username_field = get_username_field()
    username = get_username(user)

    payload = {
        'sub': username,
        'is_superuser': user.is_superuser,
        'groups': list(user.groups.all().values_list('name', flat=True)),
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'iss': api_settings.JWT_ISSUER
    }
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
    }


def get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get('email')
