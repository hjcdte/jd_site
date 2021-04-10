from rest_framework.authentication import BaseAuthentication
import jwt
from django.conf import settings


class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            name_auth = {
                        "username":payload['username'],
                        "auth":payload['first_name'],
            }
            return (name_auth, payload['id'])
        except:
            name_auth = {
                        "username":"未登录",
                        "auth":"0",
                }
            return (name_auth, "-1")