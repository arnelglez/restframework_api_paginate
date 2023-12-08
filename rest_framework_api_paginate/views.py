from django.http import JsonResponse
from django.shortcuts import render


from rest_framework import status
from rest_framework.views import APIView

from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from .mixins import MixinsList, MixinOperations
from .serializers import (
    CustomErrorSerializer,
    CustomSuccessSerializer,
    CustomResponseSerializer,
    custom_serializer,
    custom_image_serializer,
    state_serializer,
)


# Create your views here.
def list_view(modelClass, permissionGet=None, permissionPost=None, has_image=False):
    class ListView(APIView, MixinsList):
        model = modelClass
        classSerializer = (
            custom_image_serializer(model) if has_image else custom_serializer(model)
        )
        permission_get = permissionGet
        permission_post = permissionPost

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
                    result_serializer=self.classSerializer(many=True)
                ),
                404: CustomErrorSerializer,
            },
        )
        def get(self, request, *args, **kwargs):
            return super().get(request, *args, **kwargs)

        @extend_schema(
            request=self.classSerializer,
            responses={
                201: self.classSerializer,
                400: CustomErrorSerializer,
                404: CustomErrorSerializer,
            },
            parameters=[
                OpenApiParameter(
                    name="Authorization",
                    location=OpenApiParameter.HEADER,
                    description="Token used for authentication",
                    type=OpenApiTypes.STR,
                )
            ],
        )
        def post(self, request):
            return super().post(request)

    return ListView


# class AttributeOperations(APIView, MixinOperations):
#     model = Attribute
#     classSerializer = AttributeSerializer
#     classStatusSerializer = StateAttributeSerializer
#     permission_post = IsAdminUser
#     permission_put = IsAdminUser
#     permission_delete = IsAdminUser

#     @extend_schema(
#         request=AttributeSerializer,
#         responses={
#             200: AttributeSerializer,
#             400: CustomErrorSerializer,
#             404: CustomErrorSerializer,
#         },
#     )
#     def get(self, request, id):
#         return super().get(request, id)

#     @extend_schema(
#         request=StateAttributeSerializer,
#         responses={
#             202: CustomSuccessSerializer,
#             400: CustomErrorSerializer,
#             404: CustomErrorSerializer,
#         },
#     )
#     def post(self, request, id):
#         return super().post(request, id)

#     @extend_schema(
#         request=AttributeSerializer,
#         responses={
#             202: AttributeSerializer,
#             400: CustomErrorSerializer,
#             404: CustomErrorSerializer,
#         },
#         parameters=[
#             OpenApiParameter(
#                 name="Authorization",
#                 location=OpenApiParameter.HEADER,
#                 description="Token used for authentication",
#                 type=OpenApiTypes.STR,
#             )
#         ],
#     )
#     def put(self, request, id):
#         return super().put(request, id)

#     @extend_schema(
#         request=StateAttributeSerializer,
#         responses={
#             202: StateAttributeSerializer,
#             400: CustomErrorSerializer,
#             404: CustomErrorSerializer,
#         },
#     )
#     def delete(self, request, id):
#         return super().delete(request, id)
