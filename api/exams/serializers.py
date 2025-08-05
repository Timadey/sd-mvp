# serializers.py

from rest_framework import serializers
from .models import Exam, ExamProctor, Question


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        read_only_fields = ['created_by']
        exclude = ['created_at', 'updated_at']


class AssignProctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProctor
        fields = ['exam', 'proctor', 'is_primary', 'status']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
