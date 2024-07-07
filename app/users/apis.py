import logging

from typing import Any, Self
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework import serializers, status, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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

        try:
            services.register_user(
                email=input_serializer.validated_data.get('email', None),
                password=input_serializer.validated_data.get('password', None)
            )
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(
                {'message': 'There is an active user with the provided info'},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as ex:
            logger.warning({'unexpected_error': ex})
            raise APIException(ex)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        security_stamp = user.security_stamp
        token['security_stamp'] = security_stamp
        services.set_security_stamp(security_stamp)

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    class ChangePasswordInputSerializer(serializers.Serializer):
        old_password = serializers.CharField()
        new_password = serializers.CharField(validators=(
            MinLengthValidator(limit_value=8),
        ))
        confirm_password = serializers.CharField()

        def validate(self, attrs: dict) -> dict:
            new_password = attrs.get('new_password')
            confirm_password = attrs.get('confirm_password')

            if new_password != confirm_password:
                raise serializers.ValidationError(
                    'Passwords must be match.'
                )

            return attrs

    @extend_schema(request=ChangePasswordInputSerializer)    
    def post(self: Self, request: Request, *args: Any, **kwargs: Any) -> Response:
        input_serializer = self.ChangePasswordInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        if services.check_old_password(
            user=request.user,
            old_password=input_serializer.validated_data.get('old_password')
        ):
            services.set_new_password(
                user=request.user,
                new_password=input_serializer.validated_data.get('new_password')
            )
            return Response(
                {'message': 'Password has been changed successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Old password is wrong!'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
