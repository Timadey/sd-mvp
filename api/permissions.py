from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.exams.models import ExamProctor


class IsAssignedProctor(BasePermission):
    message = "You are not assigned to this exam"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        exam_id = request.data.get("exam") or view.kwargs.get("exam_id")
        return ExamProctor.objects.filter(exam_id=exam_id, proctor=request.user).exists() and request.user.role == 'proctor'


class IsAdminUser(BasePermission):
    message = "This action can be done only by admin"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'admin'