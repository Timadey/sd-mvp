from drf_spectacular.utils import OpenApiResponse

from api.core.schema import SuccessResponseSerializer, ErrorResponseSerializer
from api.exams.serializers import ExamSerializer, AssignProctorSerializer, QuestionSerializer

exam_create_schema = {
    "tags": ["Exams"],
    "request": ExamSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Exam created successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Validation error")
    },
}

assign_proctor_schema = {
    "tags": ["Exams"],
    "request": AssignProctorSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Proctor assigned successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Invalid data"),
    },
}

question_create_schema = {
    "tags": ["Questions"],
    "request": QuestionSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Question created successfully"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Unauthorized or not assigned as proctor"),
    },
}
