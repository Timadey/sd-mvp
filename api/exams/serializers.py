# serializers.py

from rest_framework import serializers
from .models import Exam, ExamProctor, Question, QuestionOption
from api.users.models import User


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'
        read_only_fields = ['created_at']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True, source='questionoption_set')
    
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_total_questions(self, obj):
        return obj.question_set.count()


class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        exclude = ['created_at', 'updated_at']


class ExamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        exclude = ['created_by', 'created_at', 'updated_at']


class ProctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email']


class ExamProctorSerializer(serializers.ModelSerializer):
    proctor_details = ProctorSerializer(source='proctor', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    
    class Meta:
        model = ExamProctor
        fields = ['id', 'exam', 'proctor', 'proctor_details', 'assigned_by', 'assigned_by_name', 
                 'exam_title', 'is_primary', 'status', 'assigned_at']
        read_only_fields = ['assigned_by', 'assigned_at']


class AssignProctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProctor
        fields = ['exam', 'proctor', 'is_primary', 'status']
        
    def validate(self, data):
        # Check if proctor is already assigned to this exam
        if ExamProctor.objects.filter(exam=data['exam'], proctor=data['proctor']).exists():
            raise serializers.ValidationError("This proctor is already assigned to this exam.")
        
        # Check if proctor role is correct
        if data['proctor'].role != 'proctor':
            raise serializers.ValidationError("Selected user must have proctor role.")
        
        return data
