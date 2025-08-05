from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.conf import settings

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('adaptive', 'Adaptive'),
        ('timed', 'Timed')
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]

    MONITORING_LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('strict', 'Strict')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField()
    max_attempts = models.PositiveIntegerField(default=1)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2)
    instructions = models.TextField(blank=True, null=True)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES, default='standard')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    proctoring_enabled = models.BooleanField(default=True)
    ai_monitoring_level = models.CharField(max_length=50, choices=MONITORING_LEVEL_CHOICES, default='standard')
    settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Exam - {self.title}"


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('code', 'Code'),
        ('image_based', 'Image-Based'),
        ('audio_based', 'Audio-Based'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    order_index = models.PositiveIntegerField()
    is_required = models.BooleanField(default=True)
    media_urls = models.JSONField(default=list)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question - {self.question_text}"


class QuestionOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order_index = models.PositiveIntegerField()
    explanation = models.TextField(blank=True)
    media_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question Option - {self.option_text}"



class ExamProctor(models.Model):
    STATUS_CHOICES = [('assigned', 'Assigned'), ('active', 'Active'), ('completed', 'Completed'),
                      ('removed', 'Removed')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    proctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_proctor', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigner', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'proctor')

    def __str__(self):
        return f"Exam Proctor - {self.exam.title} - {self.proctor.username}"

