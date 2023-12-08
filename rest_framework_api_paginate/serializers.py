from rest_framework import serializers


def create_generic_serializer(model_class):
    class Meta:
        model = model_class
        fields = "__all__"
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]

    serializer_class = type(
        f"{model_class.__name__}Serializer",
        (serializers.ModelSerializer,),
        {"Meta": Meta},
    )

    return serializer_class


def create_state_serializer(model_class):
    class Meta:
        model = model_class
        fields = "__all__"
        read_only_fields = [
            f.name for f in model_class._meta.fields if f.name != "is_active"
        ]

    serializer_class = type(
        f"{model_class.__name__}Serializer",
        (serializers.ModelSerializer,),
        {"Meta": Meta},
    )

    return serializer_class


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
