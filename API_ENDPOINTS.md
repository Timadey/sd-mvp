# Exam Management API Endpoints

This document outlines all the API endpoints for the exam management system, including admin and proctor functionalities.

## Admin Endpoints

### Exam Management

#### 1. List All Examinations
- **URL**: `GET /api/exams/`
- **Description**: Retrieve all examinations with details
- **Permission**: Admin only
- **Response**: List of exams with questions count, created by, etc.

#### 2. Get Exam Details
- **URL**: `GET /api/exams/{id}/`
- **Description**: Get detailed information about a specific exam including questions
- **Permission**: Admin only
- **Response**: Complete exam data with nested questions and options

#### 3. Create Examination
- **URL**: `POST /api/exams/create/`
- **Description**: Create a new examination
- **Permission**: Admin only
- **Request Body**:
```json
{
  "title": "Sample Exam",
  "description": "Description of the exam",
  "duration_minutes": 120,
  "max_attempts": 1,
  "passing_score": 70.00,
  "instructions": "Exam instructions",
  "exam_type": "standard",
  "status": "draft",
  "start_time": "2024-01-01T10:00:00Z",
  "end_time": "2024-01-01T12:00:00Z",
  "proctoring_enabled": true,
  "ai_monitoring_level": "standard",
  "settings": {}
}
```

#### 4. Update Examination
- **URL**: `PUT/PATCH /api/exams/{id}/update/`
- **Description**: Edit an existing examination
- **Permission**: Admin only
- **Request Body**: Same as create (partial for PATCH)

### Proctor Management

#### 5. List Available Proctors
- **URL**: `GET /api/exams/proctors/`
- **Description**: Get all users with proctor role
- **Permission**: Admin only
- **Response**: List of proctors with basic details

#### 6. Assign Proctor to Exam
- **URL**: `POST /api/exams/assign-proctor/`
- **Description**: Assign a proctor to an examination
- **Permission**: Admin only
- **Request Body**:
```json
{
  "exam": "exam_uuid",
  "proctor": 123,
  "is_primary": false,
  "status": "assigned"
}
```

#### 7. List Exam-Proctor Assignments
- **URL**: `GET /api/exams/assignments/`
- **Description**: View all proctor assignments
- **Permission**: Admin only
- **Query Parameters**:
  - `exam_id` (optional): Filter by exam
  - `proctor_id` (optional): Filter by proctor
- **Response**: List of assignments with proctor and exam details

## Proctor Endpoints

### Assigned Exams

#### 8. List Assigned Exams
- **URL**: `GET /api/exams/proctor/assigned/`
- **Description**: Get exams assigned to the logged-in proctor
- **Permission**: Proctor only
- **Response**: List of exams assigned to the proctor

### Question Management

#### 9. Add Question to Exam
- **URL**: `POST /api/exams/questions/create/`
- **Description**: Add a question to an assigned exam
- **Permission**: Proctor (must be assigned to the exam)
- **Request Body**:
```json
{
  "exam": "exam_uuid",
  "question_text": "What is the capital of France?",
  "question_type": "multiple_choice",
  "points": 1.0,
  "time_limit_seconds": 60,
  "order_index": 1,
  "is_required": true,
  "media_urls": [],
  "metadata": {}
}
```

#### 10. List Questions for Exam
- **URL**: `GET /api/exams/{exam_id}/questions/`
- **Description**: Get all questions for a specific exam
- **Permission**: Admin or assigned proctor
- **Response**: List of questions with options

#### 11. Add Question Option
- **URL**: `POST /api/exams/question-options/create/`
- **Description**: Add an option to a question
- **Permission**: Admin or proctor assigned to the exam containing the question
- **Request Body**:
```json
{
  "question": "question_uuid",
  "option_text": "Paris",
  "is_correct": true,
  "order_index": 1,
  "explanation": "Paris is the capital of France",
  "media_url": ""
}
```

## Response Format

All endpoints return responses in the following format:

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {...}
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "errors": [...]
}
```

## Authentication

All endpoints require authentication using JWT tokens:
```
Authorization: Bearer {your_jwt_token}
```

## Permission System

- **Admin**: Can perform all operations
- **Proctor**: Can only manage questions for assigned exams
- **Candidate**: No access to these endpoints

## Validation Rules

### Proctor Assignment
- Proctor cannot be assigned to the same exam twice
- Only users with 'proctor' role can be assigned as proctors

### Question Management
- Proctors can only add questions to exams they are assigned to
- Question options can only be added to questions in exams the proctor is assigned to

## Usage Examples

### Creating an Exam and Assigning a Proctor (Admin)

1. Create exam:
```bash
POST /api/exams/create/
```

2. Assign proctor:
```bash
POST /api/exams/assign-proctor/
{
  "exam": "created_exam_uuid",
  "proctor": 123,
  "is_primary": true,
  "status": "assigned"
}
```

### Adding Questions with Options (Proctor)

1. Add question:
```bash
POST /api/exams/questions/create/
{
  "exam": "assigned_exam_uuid",
  "question_text": "What is 2+2?",
  "question_type": "multiple_choice",
  "points": 1.0,
  "order_index": 1
}
```

2. Add options:
```bash
POST /api/exams/question-options/create/
{
  "question": "created_question_uuid",
  "option_text": "4",
  "is_correct": true,
  "order_index": 1
}
```

## Status Codes

- **200**: OK
- **201**: Created
- **400**: Bad Request
- **403**: Forbidden
- **404**: Not Found
- **500**: Internal Server Error
