import logging
import jwt

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.conf import settings

from core import services

logger = logging.getLogger('backend')

class SecurityStampChecker:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
    
    def __call__(self, request: Request) -> Response:
        if request.META.get('HTTP_AUTHORIZATION'):
            auth_token = str(request.META['HTTP_AUTHORIZATION']).split(' ')[1]
            try:
                data = jwt.decode(jwt=auth_token, key=settings.SECRET_KEY, algorithms="HS256")
                security_stamp = data.get('security_stamp')
                if (services.get_security_stamp(security_stamp)) == False:
                    response: Response = Response(
                        data='Unauthorized',
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
                    return response
            except Exception as ex:
                logger.warning(f'Cannot decode JWT => {ex}')

        response = self.get_response(request)

        return response