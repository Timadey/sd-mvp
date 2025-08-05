# urls.py

from django.urls import path
from .views import ExamCreateAPIView, AssignProctorAPIView, QuestionCreateAPIView

urlpatterns = [
    path('create/', ExamCreateAPIView.as_view(), name='exam-create'),
    path('assign-proctor/', AssignProctorAPIView.as_view(), name='assign-proctor'),
    path('questions/create/', QuestionCreateAPIView.as_view(), name='question-create'),
]
