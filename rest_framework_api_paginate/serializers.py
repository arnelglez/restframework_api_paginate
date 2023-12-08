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
            f.name for f in Contact._meta.fields if f.name != "is_active"
        ]

    serializer_class = type(
        f"{model_class.__name__}Serializer",
        (serializers.ModelSerializer,),
        {"Meta": Meta},
    )

    return serializer_class
