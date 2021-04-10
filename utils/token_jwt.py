import jwt, datetime
from django.conf import settings

def create_jwttoken(payload, timeout=1):
    headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
    
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=timeout)

    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256", headers=headers)
    return token
