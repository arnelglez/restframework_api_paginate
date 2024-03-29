from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from .serializers import (
    CustomErrorSerializer,
    CustomSuccessSerializer,
    CustomResponseSerializer,
)


def common_get_list_schema(*args, **kwargs):
    classSerializer = kwargs.pop("serializer")
    common_kwargs = {
        "parameters": [
            OpenApiParameter(
                name="page", description="Page number", required=False, type=int
            ),
            OpenApiParameter(
                name="query", description="Search word", required=False, type=str
            ),
            OpenApiParameter(
                name="order", description="Order by Column", required=False, type=str
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
        "responses": {
            200: CustomResponseSerializer(result_serializer=classSerializer(many=True)),
            400: CustomErrorSerializer,
            404: CustomErrorSerializer,
        },
    }
    common_kwargs.update(kwargs)
    return extend_schema(*args, **common_kwargs)


def common_post_list_schema(*args, **kwargs):
    classSerializer = kwargs.pop("serializer")
    common_kwargs = {
        "request": classSerializer,
        "responses": {
            201: classSerializer,
            400: CustomErrorSerializer,
            404: CustomErrorSerializer,
        },
        "parameters": [
            OpenApiParameter(
                name="Authorization",
                location=OpenApiParameter.HEADER,
                description="Token used for authentication",
                type=OpenApiTypes.STR,
            )
        ],
    }
    common_kwargs.update(kwargs)
    return extend_schema(*args, **common_kwargs)


def common_get_operation_schema(*args, **kwargs):
    classSerializer = kwargs.pop("serializer")
    common_kwargs = {
        "request": classSerializer,
        "responses": {
            200: classSerializer,
            400: CustomErrorSerializer,
            404: CustomErrorSerializer,
        },
    }
    common_kwargs.update(kwargs)
    return extend_schema(*args, **common_kwargs)


def common_post_operation_schema(*args, **kwargs):
    classSerializer = kwargs.pop("serializer")
    common_kwargs = {
        "request": classSerializer,
        "responses": {
            200: classSerializer,
            400: CustomErrorSerializer,
            404: CustomErrorSerializer,
        },
    }
    common_kwargs.update(kwargs)
    return extend_schema(*args, **common_kwargs)


def common_put_operation_schema(*args, **kwargs):
    classSerializer = kwargs.pop("serializer", None)
    common_kwargs = {
        "request": classSerializer,
        "responses": {
            202: classSerializer,
            400: CustomErrorSerializer,
            404: CustomErrorSerializer,
        },
        "parameters": [
            OpenApiParameter(
                name="Authorization",
                location=OpenApiParameter.HEADER,
                description="Token used for authentication",
                type=OpenApiTypes.STR,
            )
        ],
    }
    common_kwargs.update(kwargs)
    return extend_schema(*args, **common_kwargs)


def common_delete_operation_schema(*args, **kwargs):
    classSerializer = kwargs.pop("serializer")
    common_kwargs = {
        "request": classSerializer,
        "responses": {
            202: classSerializer,
            400: CustomErrorSerializer,
            404: CustomErrorSerializer,
        },
    }
    common_kwargs.update(kwargs)
    return extend_schema(*args, **common_kwargs)
