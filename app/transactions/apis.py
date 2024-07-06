import logging

from typing import Self, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers, permissions
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema

from core import selectors

logger = logging.getLogger('backend')


class AllTransactions(APIView):
    permission_classes = [permissions.IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        amount = serializers.FloatField()

    @extend_schema(responses=OutputSerializer)
    def get(self: Self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            queryset = selectors.list_transactions()
        except Exception as ex:
            logger.warning(ex)
            raise APIException(
                {'message': f'Database error >> {ex}'}
            )
        response = self.OutputSerializer(queryset, many=True).data
        return Response(response, status=status.HTTP_200_OK)
