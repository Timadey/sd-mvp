#!/usr/bin/env python3
"""
Test script for the Exam Management System

This script demonstrates the functionality of the exam management system
by creating test data and testing API endpoints.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.users.models import User
from api.exams.models import Exam, ExamProctor, Question, QuestionOption
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_data():
    """Create test users and data"""
    print("Creating test data...")
    
    # Create admin user if not exists
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("✓ Admin user created")
    else:
        print("✓ Admin user already exists")
    
    # Create proctor users
    proctors = []
    for i in range(1, 4):
        proctor, created = User.objects.get_or_create(
            username=f'proctor{i}',
            defaults={
                'email': f'proctor{i}@example.com',
                'first_name': f'Proctor',
                'last_name': f'User{i}',
                'role': 'proctor'
            }
        )
        if created:
            proctor.set_password('proctor123')
            proctor.save()
            print(f"✓ Proctor {i} created")
        proctors.append(proctor)
    
    # Create sample exams
    sample_exams = [
        {
            'title': 'Mathematics Final Exam',
            'description': 'Comprehensive mathematics examination covering algebra and calculus',
            'duration_minutes': 120,
            'passing_score': 70.00,
            'exam_type': 'standard',
            'status': 'published'
        },
        {
            'title': 'Python Programming Assessment',
            'description': 'Programming skills assessment for Python developers',
            'duration_minutes': 90,
            'passing_score': 75.00,
            'exam_type': 'timed',
            'status': 'draft'
        },
        {
            'title': 'Database Design Quiz',
            'description': 'Quick assessment on database design principles',
            'duration_minutes': 45,
            'passing_score': 80.00,
            'exam_type': 'standard',
            'status': 'published'
        }
    ]
    
    exams = []
    for exam_data in sample_exams:
        exam, created = Exam.objects.get_or_create(
            title=exam_data['title'],
            defaults={
                **exam_data,
                'created_by': admin,
                'start_time': datetime.now() + timedelta(days=1),
                'end_time': datetime.now() + timedelta(days=8),
                'instructions': f"Instructions for {exam_data['title']}",
                'proctoring_enabled': True,
                'ai_monitoring_level': 'standard',
                'settings': {}
            }
        )
        if created:
            print(f"✓ Exam '{exam.title}' created")
        exams.append(exam)
    
    # Assign proctors to exams
    assignments = [
        (exams[0], proctors[0], True),   # Math exam -> Proctor 1 (primary)
        (exams[0], proctors[1], False),  # Math exam -> Proctor 2 (secondary)
        (exams[1], proctors[1], True),   # Python exam -> Proctor 2 (primary)
        (exams[2], proctors[2], True),   # Database exam -> Proctor 3 (primary)
    ]
    
    for exam, proctor, is_primary in assignments:
        assignment, created = ExamProctor.objects.get_or_create(
            exam=exam,
            proctor=proctor,
            defaults={
                'assigned_by': admin,
                'is_primary': is_primary,
                'status': 'assigned'
            }
        )
        if created:
            print(f"✓ Assigned {proctor.username} to '{exam.title}' (Primary: {is_primary})")
    
    return admin, proctors, exams

def create_sample_questions():
    """Create sample questions and options"""
    print("\nCreating sample questions...")
    
    # Get the math exam
    math_exam = Exam.objects.get(title='Mathematics Final Exam')
    
    # Sample questions for math exam
    questions_data = [
        {
            'question_text': 'What is the derivative of x²?',
            'question_type': 'multiple_choice',
            'points': 2.0,
            'order_index': 1,
            'options': [
                ('2x', True, 'Correct! The derivative of x² is 2x'),
                ('x', False, 'Incorrect. This would be the derivative of x²/2'),
                ('x²', False, 'Incorrect. This is the original function'),
                ('2', False, 'Incorrect. This would be the derivative of 2x')
            ]
        },
        {
            'question_text': 'Solve for x: 2x + 5 = 13',
            'question_type': 'multiple_choice',
            'points': 1.5,
            'order_index': 2,
            'options': [
                ('x = 4', True, 'Correct! 2(4) + 5 = 13'),
                ('x = 3', False, 'Incorrect. 2(3) + 5 = 11'),
                ('x = 5', False, 'Incorrect. 2(5) + 5 = 15'),
                ('x = 6', False, 'Incorrect. 2(6) + 5 = 17')
            ]
        },
        {
            'question_text': 'What is the integral of 2x?',
            'question_type': 'short_answer',
            'points': 3.0,
            'order_index': 3,
            'options': []  # No options for short answer
        }
    ]
    
    for question_data in questions_data:
        question, created = Question.objects.get_or_create(
            exam=math_exam,
            question_text=question_data['question_text'],
            defaults={
                'question_type': question_data['question_type'],
                'points': question_data['points'],
                'order_index': question_data['order_index'],
                'is_required': True,
                'media_urls': [],
                'metadata': {}
            }
        )
        
        if created:
            print(f"✓ Question created: {question.question_text}")
            
            # Add options if it's a multiple choice question
            for idx, (option_text, is_correct, explanation) in enumerate(question_data['options']):
                option = QuestionOption.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=is_correct,
                    order_index=idx + 1,
                    explanation=explanation
                )
                print(f"  ✓ Option: {option_text} ({'Correct' if is_correct else 'Incorrect'})")

def display_summary():
    """Display summary of created data"""
    print("\n" + "="*60)
    print("EXAM MANAGEMENT SYSTEM - TEST DATA SUMMARY")
    print("="*60)
    
    print(f"\n📊 STATISTICS:")
    print(f"   Users: {User.objects.count()}")
    print(f"   - Admins: {User.objects.filter(role='admin').count()}")
    print(f"   - Proctors: {User.objects.filter(role='proctor').count()}")
    print(f"   Exams: {Exam.objects.count()}")
    print(f"   Questions: {Question.objects.count()}")
    print(f"   Question Options: {QuestionOption.objects.count()}")
    print(f"   Proctor Assignments: {ExamProctor.objects.count()}")
    
    print(f"\n📚 EXAMS:")
    for exam in Exam.objects.all():
        question_count = exam.question_set.count()
        proctor_count = exam.examproctor_set.count()
        print(f"   • {exam.title}")
        print(f"     Status: {exam.status.title()}")
        print(f"     Questions: {question_count}")
        print(f"     Assigned Proctors: {proctor_count}")
        print(f"     Duration: {exam.duration_minutes} minutes")
    
    print(f"\n👥 PROCTOR ASSIGNMENTS:")
    for assignment in ExamProctor.objects.all():
        role = "Primary" if assignment.is_primary else "Secondary"
        print(f"   • {assignment.proctor.get_full_name()} -> {assignment.exam.title} ({role})")
    
    print(f"\n🔗 API ENDPOINTS READY:")
    print(f"   • GET  /api/exams/ - List all exams (Admin)")
    print(f"   • POST /api/exams/create/ - Create exam (Admin)")
    print(f"   • GET  /api/exams/proctors/ - List proctors (Admin)")
    print(f"   • POST /api/exams/assign-proctor/ - Assign proctor (Admin)")
    print(f"   • GET  /api/exams/proctor/assigned/ - Assigned exams (Proctor)")
    print(f"   • POST /api/exams/questions/create/ - Add question (Proctor)")
    print(f"   • POST /api/exams/question-options/create/ - Add option (Proctor)")
    
    print(f"\n🔑 TEST CREDENTIALS:")
    print(f"   Admin: username='admin', password='admin123'")
    print(f"   Proctor 1: username='proctor1', password='proctor123'")
    print(f"   Proctor 2: username='proctor2', password='proctor123'")
    print(f"   Proctor 3: username='proctor3', password='proctor123'")
    
    print(f"\n🌐 SWAGGER DOCS:")
    print(f"   http://127.0.0.1:8000/api/docs/swagger/")
    
    print("\n" + "="*60)

def main():
    print("🚀 Setting up Exam Management System Test Data")
    print("="*60)
    
    try:
        admin, proctors, exams = create_test_data()
        create_sample_questions()
        display_summary()
        
        print("✅ Test data setup completed successfully!")
        print("\n💡 You can now:")
        print("   1. Start the Django server: python manage.py runserver")
        print("   2. Visit the API docs: http://127.0.0.1:8000/api/docs/swagger/")
        print("   3. Test the endpoints using the credentials above")
        print("   4. Login as admin to view all exams and manage proctors")
        print("   5. Login as proctor to see assigned exams and add questions")
        
    except Exception as e:
        print(f"❌ Error setting up test data: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
