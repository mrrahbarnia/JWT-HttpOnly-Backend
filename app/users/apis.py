import logging

from typing import Any
from django.core.validators import MinLengthValidator
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from core import services

logger = logging.getLogger('backend')


class RegisterApi(APIView):

    class RegisterInputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(validators=(
                MinLengthValidator(limit_value=8), 
            )
        )
        confirm_password = serializers.CharField()

        def validate(self, attrs: dict) -> dict:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            if password != confirm_password:
                raise serializers.ValidationError(
                    'Passwords must be match.'
                )
            return attrs

    @extend_schema(request=RegisterInputSerializer)
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        input_serializer = self.RegisterInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        services.register_user(
            email=input_serializer.validated_data.get('email', None),
            password=input_serializer.validated_data.get('password', None)
        )

        return Response(status=status.HTTP_201_CREATED)
