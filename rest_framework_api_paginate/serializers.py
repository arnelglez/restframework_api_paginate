from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class CustomSerializer:
    model = None

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)

    image = Base64ImageField(required=False)

    class Meta:
        model = self.model
        fields = "__all__"
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]


class StateCustomSerializer:
    model = None

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = self.model
        fields = "__all__"
        read_only_fields = [
            f.name for f in self.model._meta.fields if f.name != "is_active"
        ]


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
