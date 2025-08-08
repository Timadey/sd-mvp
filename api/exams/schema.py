from drf_spectacular.utils import OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.core.schema import SuccessResponseSerializer, ErrorResponseSerializer
from api.exams.serializers import (
    ExamSerializer, ExamCreateSerializer, ExamUpdateSerializer, AssignProctorSerializer, 
    QuestionSerializer, QuestionCreateSerializer, QuestionOptionSerializer,
    ExamProctorSerializer
)

# Admin Exam Schemas
exam_list_schema = {
    "tags": ["Admin - Exams"],
    "responses": {
        200: OpenApiResponse(response=SuccessResponseSerializer, description="Exams retrieved successfully"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Admin access required"),
    },
}

exam_detail_schema = {
    "tags": ["Admin - Exams"],
    "responses": {
        200: OpenApiResponse(response=SuccessResponseSerializer, description="Exam details retrieved successfully"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Admin access required"),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Exam not found"),
    },
}

exam_create_schema = {
    "tags": ["Admin - Exams"],
    "request": ExamCreateSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Exam created successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Validation error"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Admin access required"),
    },
}

exam_update_schema = {
    "tags": ["Admin - Exams"],
    "request": ExamUpdateSerializer,
    "responses": {
        200: OpenApiResponse(response=SuccessResponseSerializer, description="Exam updated successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Validation error"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Admin access required"),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Exam not found"),
    },
}

# Admin Proctor Assignment Schemas
exam_proctor_list_schema = {
    "tags": ["Admin - Proctor Management"],
    "parameters": [
        OpenApiParameter(
            name="exam_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description="Filter by exam ID",
            required=False,
        ),
        OpenApiParameter(
            name="proctor_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter by proctor ID",
            required=False,
        ),
    ],
    "responses": {
        200: OpenApiResponse(response=SuccessResponseSerializer, description="Exam-proctor assignments retrieved successfully"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Admin access required"),
    },
}

assign_proctor_schema = {
    "tags": ["Admin - Proctor Management"],
    "request": AssignProctorSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Proctor assigned successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Invalid data or proctor already assigned"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Admin access required"),
    },
}

# Proctor Question Schemas
question_create_schema = {
    "tags": ["Proctor - Questions"],
    "request": QuestionCreateSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Question created successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Validation error"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Not assigned as proctor to this exam"),
    },
}

question_list_schema = {
    "tags": ["Proctor - Questions"],
    "parameters": [
        OpenApiParameter(
            name="exam_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
            description="Exam ID",
            required=True,
        ),
    ],
    "responses": {
        200: OpenApiResponse(response=SuccessResponseSerializer, description="Questions retrieved successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Exam ID required"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Not assigned as proctor to this exam"),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Exam not found"),
    },
}

question_option_create_schema = {
    "tags": ["Proctor - Question Options"],
    "request": QuestionOptionSerializer,
    "responses": {
        201: OpenApiResponse(response=SuccessResponseSerializer, description="Question option created successfully"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Validation error or question ID required"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Not assigned as proctor to this exam"),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Question not found"),
    },
}

# Proctor Exam Schemas
proctor_exam_list_schema = {
    "tags": ["Proctor - Assigned Exams"],
    "responses": {
        200: OpenApiResponse(response=SuccessResponseSerializer, description="Assigned exams retrieved successfully"),
        403: OpenApiResponse(response=ErrorResponseSerializer, description="Proctor access required"),
    },
}
