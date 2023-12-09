from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from .serializers import (
    CustomErrorSerializer,
    CustomSuccessSerializer,
    CustomResponseSerializer,
    custom_serializer,
    state_serializer,
)


def common_get_many_schema(classSerializer):
    def decorator(func):
        @extend_schema(
            parameters=[
                OpenApiParameter(
                    name="page", description="Page number", required=False, type=int
                ),
                OpenApiParameter(
                    name="page_size",
                    description="Items per page",
                    required=False,
                    type=int,
                ),
                OpenApiParameter(
                    name="active",
                    description="Filter by active",
                    required=False,
                    type=bool,
                ),
            ],
            responses={
                200: CustomResponseSerializer(
                    result_serializer=classSerializer(many=True)
                ),
                400: CustomErrorSerializer,
                404: CustomErrorSerializer,
            },
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
