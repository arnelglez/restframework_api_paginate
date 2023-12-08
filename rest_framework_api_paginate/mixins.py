from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms import ValidationError


from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes


from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.db import models


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    # We won't set a default page_size here since it will be dynamic

    def paginate_queryset(self, queryset, request, view=None):
        # Check if a page number is provided in the request
        page_number = request.query_params.get(self.page_query_param)

        if page_number is not None:
            # If no page number is provided, set the page_size to the total count
            self.page_size = queryset.count()
        else:
            # Otherwise, try to get the page_size from the request
            # or use the default if it's not provided
            try:
                self.page_size = int(
                    request.query_params.get(self.page_size_query_param, self.page_size)
                )
            except (TypeError, ValueError):
                self.page_size = self.get_default_page_size()

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data, count):
        return JsonResponse(
            {
                "count": count,
                "next": None if count == 0 else self.get_next_link(),
                "previous": None if count == 0 else self.get_previous_link(),
                "results": data,
            },
            safe=False,
            status=status.HTTP_200_OK,
        )


class MixinsList:
    model = None
    classSerializer = None
    permission_get = None
    permission_post = None

    permission_classes = [permission_get]

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
            200: CustomResponseSerializer(result_serializer=classSerializer(many=True)),
            404: CustomErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Mixin function to list every objects of any model
        """

        active = request.query_params.get("active", None)

        if active is not None:
            active = True if active.lower() == "true" else False
            objects = self.model.objects.filter(is_active=bool(active)).order_by("id")
        else:
            objects = self.model.objects.all().order_by("id")

        total_count = objects.count()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(objects, request)

        if page is not None:
            serializers = self.classSerializer(page, many=True)
            return paginator.get_paginated_response(serializers.data, total_count)
        elif total_count == 0:
            return paginator.get_paginated_response([], total_count)
        return JsonResponse(
            {"detail": "Invalid page."}, status=status.HTTP_404_NOT_FOUND
        )

    permission_classes = [permission_post]

    @extend_schema(
        request=classSerializer,
        responses={
            201: classSerializer,
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
        """
        Mixin function to create object of any model
        """
        # serializes data entry
        objSerializer = self.classSerializer(data=request.data)
        # verify if entry is valid
        if objSerializer.is_valid():
            # save entry
            objSerializer.save()
            # show object saved
            return JsonResponse(
                objSerializer.data, safe=False, status=status.HTTP_201_CREATED
            )
        # show errors because not save
        return JsonResponse(
            objSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
        )


class MixinOperations:
    model = None
    classSerializer = None
    classStateSerializer = None
    permission_get = None
    permission_post = None
    permission_put = None
    permission_delete = None

    def get(self, request, id):
        """
        Mixin function to show one objects of any model by his id
        """
        # Search object by id
        obj = get_object_or_404(self.model, id=id)
        # serializes object
        serializer = self.classSerializer(obj, many=False)
        # show object
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    permission_classes = [permission_post]

    def post(self, request, id):
        """
        Mixin function to active one objects of any model by his id
        """
        obj = get_object_or_404(self.model, id=id)
        if not obj.is_active:
            # activating deleted user
            objActive = {"is_active": 1}
            # serializes data entry
            serializer = self.classStateSerializer(obj, data=objActive)
            # verify if entry is valid
            if serializer.is_valid():
                # save entry
                serializer.save()
                # show blank object (deleted)
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_202_ACCEPTED
                )
            # show errors because not save
            return JsonResponse(
                serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
            )
            # show errors because user is inactive
        return JsonResponse(
            {"detail": f"This {self.model.__name__} is active"},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )

    permission_classes = [permission_put]

    def put(self, request, id):
        """
        Mixin function to edit one objects of any model by his id
        """
        # Search object by id
        obj = get_object_or_404(self.model, id=id)

        # serializes data entry
        serializer = self.classSerializer(obj, data=request.data)

        # verify if entry is valid
        if serializer.is_valid():
            # save entry
            serializer.save()
            # show object updated
            return JsonResponse(
                serializer.data, safe=False, status=status.HTTP_202_ACCEPTED
            )
        # show errors because not save
        return JsonResponse(
            serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
        )

    permission_classes = [permission_delete]

    def delete(self, request, id):
        """
        Mixin function to delete one objects of any model by his id
        """
        # Search object by id
        obj = get_object_or_404(self.model, id=id)
        if obj.is_active:
            # user can be deleted only status inactive
            objDelete = {"is_active": 0}
            # serializes data entry
            serializer = self.classStateSerializer(obj, data=objDelete)
            # verify if entry is valid
            if serializer.is_valid():
                # save entry
                serializer.save()
                # show blank object (deleted)
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_202_ACCEPTED
                )
            # show errors because not save
            return JsonResponse(
                serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
            )
            # show errors because user is inactive
        return JsonResponse(
            {"detail": f"This {self.model.__name__} is inactive"},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )
