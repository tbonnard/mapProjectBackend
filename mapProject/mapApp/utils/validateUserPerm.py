from rest_framework.exceptions import AuthenticationFailed

import jwt

from ..models import User


def validate_if_authenticated(request):
    token = request.COOKIES.get('jwtTk')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'BTNN02En7EFUV4tsNzOq68hVspfLa9DeRGc6kYTJr5q6Xsrn1Yi2lfJQurB0', algorithms=['HS256'])
        user = User.objects.get(pk=payload['id'])
        obj = {
            'authenticated': True,
            'user': user
        }
        return obj
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

def validate_superuser(user):
    user_to_validate = User.objects.get(pk=user.id)
    if user_to_validate.is_superuser:
        return True
    return False

