# urls.py

from django.urls import path
from .views import (
    # Admin views
    ExamListAPIView, ExamDetailAPIView, ExamCreateAPIView, ExamUpdateAPIView,
    ExamProctorListAPIView, AssignProctorAPIView, ProctorListAPIView,
    # Proctor views
    ProctorExamListAPIView, QuestionCreateAPIView, QuestionListAPIView, QuestionOptionCreateAPIView
)

urlpatterns = [
    # Admin - Exam Management
    path('', ExamListAPIView.as_view(), name='exam-list'),
    path('<uuid:id>/', ExamDetailAPIView.as_view(), name='exam-detail'),
    path('create/', ExamCreateAPIView.as_view(), name='exam-create'),
    path('<uuid:id>/update/', ExamUpdateAPIView.as_view(), name='exam-update'),
    
    # Admin - Proctor Management
    path('proctors/', ProctorListAPIView.as_view(), name='proctor-list'),
    path('assign-proctor/', AssignProctorAPIView.as_view(), name='assign-proctor'),
    path('assignments/', ExamProctorListAPIView.as_view(), name='exam-proctor-list'),
    
    # Proctor - Assigned Exams
    path('proctor/assigned/', ProctorExamListAPIView.as_view(), name='proctor-exam-list'),
    
    # Proctor - Question Management
    path('questions/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('<uuid:exam_id>/questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('question-options/create/', QuestionOptionCreateAPIView.as_view(), name='question-option-create'),
]
