from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from api import permissions
from api.core.responses import success, error
from api.exams.models import Exam, ExamProctor, Question, QuestionOption
from api.exams.schema import (
    exam_create_schema, assign_proctor_schema, question_create_schema,
    exam_list_schema, exam_detail_schema, exam_update_schema,
    question_option_create_schema, exam_proctor_list_schema
)
from api.exams.serializers import (
    ExamSerializer, ExamCreateSerializer, ExamUpdateSerializer, AssignProctorSerializer, 
    QuestionSerializer, QuestionCreateSerializer, QuestionOptionSerializer,
    ExamProctorSerializer
)
from api.permissions import IsAssignedProctor
from api.users.models import User


# Admin Views
class ExamListAPIView(generics.ListAPIView):
    """Admin view to list all examinations"""
    queryset = Exam.objects.all().order_by('-created_at')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(**exam_list_schema)
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return success(response.data, "Exams retrieved successfully")


class ExamDetailAPIView(generics.RetrieveAPIView):
    """Admin view to get detailed exam information"""
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    lookup_field = 'id'

    @extend_schema(**exam_detail_schema)
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return success(response.data, "Exam details retrieved successfully")


class ExamCreateAPIView(generics.CreateAPIView):
    """Admin view to create new examinations"""
    queryset = Exam.objects.all()
    serializer_class = ExamCreateSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(**exam_create_schema)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success(response.data, "Exam created successfully", status.HTTP_201_CREATED)


class ExamUpdateAPIView(generics.UpdateAPIView):
    """Admin view to edit examinations"""
    queryset = Exam.objects.all()
    serializer_class = ExamUpdateSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    lookup_field = 'id'

    @extend_schema(**exam_update_schema)
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return success(response.data, "Exam updated successfully")

    @extend_schema(**exam_update_schema)
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return success(response.data, "Exam updated successfully")


class ExamProctorListAPIView(generics.ListAPIView):
    """Admin view to list all exam-proctor assignments"""
    queryset = ExamProctor.objects.all().order_by('-assigned_at')
    serializer_class = ExamProctorSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        exam_id = self.request.query_params.get('exam_id')
        proctor_id = self.request.query_params.get('proctor_id')
        
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        if proctor_id:
            queryset = queryset.filter(proctor_id=proctor_id)
        
        return queryset

    @extend_schema(**exam_proctor_list_schema)
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return success(response.data, "Exam-proctor assignments retrieved successfully")


class AssignProctorAPIView(generics.CreateAPIView):
    """Admin view to assign proctors to exams"""
    queryset = ExamProctor.objects.all()
    serializer_class = AssignProctorSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @extend_schema(**assign_proctor_schema)
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return success(response.data, "Proctor assigned successfully", status.HTTP_201_CREATED)
        except Exception as e:
            return error(str(e), status.HTTP_400_BAD_REQUEST)


class ProctorListAPIView(generics.ListAPIView):
    """Admin view to list all available proctors"""
    queryset = User.objects.filter(role='proctor').order_by('first_name', 'last_name')
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        proctors = self.get_queryset()
        data = [{
            'id': proctor.id,
            'username': proctor.username,
            'first_name': proctor.first_name,
            'last_name': proctor.last_name,
            'full_name': proctor.get_full_name(),
            'email': proctor.email,
        } for proctor in proctors]
        return success(data, "Available proctors retrieved successfully")


# Proctor Views
class ProctorExamListAPIView(generics.ListAPIView):
    """Proctor view to list assigned exams"""
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'proctor':
            return Exam.objects.none()
        
        # Get exams assigned to this proctor
        exam_ids = ExamProctor.objects.filter(
            proctor=self.request.user,
            status__in=['assigned', 'active']
        ).values_list('exam_id', flat=True)
        
        return Exam.objects.filter(id__in=exam_ids).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        if request.user.role != 'proctor':
            return error("Only proctors can access this endpoint", status.HTTP_403_FORBIDDEN)
        
        response = super().get(request, *args, **kwargs)
        return success(response.data, "Assigned exams retrieved successfully")


class QuestionCreateAPIView(generics.CreateAPIView):
    """Proctor view to add questions to assigned exams"""
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAuthenticated, IsAssignedProctor]

    @extend_schema(**question_create_schema)
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return success(response.data, "Question created successfully", status.HTTP_201_CREATED)
        except Exception as e:
            return error(str(e), status.HTTP_400_BAD_REQUEST)


class QuestionListAPIView(generics.ListAPIView):
    """Proctor view to list questions for an assigned exam"""
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        exam_id = self.kwargs.get('exam_id')
        
        if self.request.user.role == 'admin':
            return Question.objects.filter(exam_id=exam_id).order_by('order_index')
        elif self.request.user.role == 'proctor':
            # Check if proctor is assigned to this exam
            if ExamProctor.objects.filter(exam_id=exam_id, proctor=self.request.user).exists():
                return Question.objects.filter(exam_id=exam_id).order_by('order_index')
        
        return Question.objects.none()

    def get(self, request, *args, **kwargs):
        exam_id = self.kwargs.get('exam_id')
        if not exam_id:
            return error("Exam ID is required", status.HTTP_400_BAD_REQUEST)
        
        # Verify exam exists
        if not Exam.objects.filter(id=exam_id).exists():
            return error("Exam not found", status.HTTP_404_NOT_FOUND)
        
        response = super().get(request, *args, **kwargs)
        return success(response.data, "Questions retrieved successfully")


class QuestionOptionCreateAPIView(generics.CreateAPIView):
    """Proctor view to add options to questions in assigned exams"""
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        question_id = request.data.get('question')
        
        if not question_id:
            return error("Question ID is required", status.HTTP_400_BAD_REQUEST)
        
        try:
            question = get_object_or_404(Question, id=question_id)
            
            # Check if user has permission to add options to this question
            if request.user.role == 'admin':
                pass  # Admin can add options to any question
            elif request.user.role == 'proctor':
                # Check if proctor is assigned to the exam that contains this question
                if not ExamProctor.objects.filter(exam=question.exam, proctor=request.user).exists():
                    return error("You are not assigned to this exam", status.HTTP_403_FORBIDDEN)
            else:
                return error("You don't have permission to perform this action", status.HTTP_403_FORBIDDEN)
            
            response = super().create(request, *args, **kwargs)
            return success(response.data, "Question option created successfully", status.HTTP_201_CREATED)
            
        except Exception as e:
            return error(str(e), status.HTTP_400_BAD_REQUEST)

    @extend_schema(**question_option_create_schema)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
