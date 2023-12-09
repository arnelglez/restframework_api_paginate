from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


def custom_serializer(modelClass):
    class_name = f"{modelClass.__name__}Serializer"

    # Define the Meta class with model and fields information, including read_only_fields
    MetaClass = type(
        "Meta",
        (),
        {
            "model": modelClass,
            "fields": "__all__",
            "read_only_fields": ["id", "is_active", "created_at", "updated_at"],
        },
    )

    # Create and return the serializer class
    return type(class_name, (serializers.ModelSerializer,), {"Meta": MetaClass})


def custom_image_serializer(modelClass, image_field_name):
    class CustomImageSerializer(serializers.ModelSerializer):
        if image_field_name:
            vars()[image_field_name] = CustomImageField(required=False, allow_null=True)

        class Meta:
            model = modelClass
            fields = "__all__"
            read_only_fields = ["id", "is_active", "created_at", "updated_at"]

    return CustomImageSerializer


def state_serializer(modelClass):
    class StateSerializer(serializers.ModelSerializer):
        class Meta:
            model = modelClass
            fields = "__all__"
            read_only_fields = [
                f.name for f in modelClass._meta.fields if f.name != "is_active"
            ]

    return StateSerializer


class CustomErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class CustomSuccessSerializer(serializers.Serializer):
    message = serializers.CharField()


class CustomResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(required=False, allow_null=True)
    previous = serializers.URLField(required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        result_serializer = kwargs.pop("result_serializer", serializers.Serializer())
        super().__init__(*args, **kwargs)
        self.fields["results"] = result_serializer
