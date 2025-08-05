# api/exams/schemas.py

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema_serializer
from rest_framework import serializers

# Custom wrapper response format
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Success Example",
            value={
                "status": "success",
                "message": "Operation completed successfully",
                "data": {"example_field": "example_value"}
            }
        )
    ]
)
class SuccessResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Error Example",
            value={
                "status": "error",
                "message": "Something went wrong",
                "data": None
            }
        )
    ]
)
class ErrorResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False)
