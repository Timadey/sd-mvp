from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from api import permissions
from api.core.responses import success
from api.exams.models import Exam, ExamProctor, Question
from api.exams.schema import exam_create_schema, assign_proctor_schema, question_create_schema
from api.exams.serializers import ExamSerializer, AssignProctorSerializer, QuestionSerializer
from api.permissions import IsAssignedProctor


# Create your views here.
class ExamCreateAPIView(generics.CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(**exam_create_schema)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success(response.data, "Exam created successfully", status.HTTP_201_CREATED)

class AssignProctorAPIView(generics.CreateAPIView):
    queryset = ExamProctor.objects.all()
    serializer_class = AssignProctorSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @extend_schema(**assign_proctor_schema)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success(response.data, "Proctor assigned successfully")

class QuestionCreateAPIView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAssignedProctor]

    @extend_schema(**question_create_schema)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success(response.data, "Question created successfully", status.HTTP_201_CREATED)