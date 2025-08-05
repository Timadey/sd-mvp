from rest_framework.exceptions import APIException
from rest_framework import status

class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad_request"

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found."
    default_code = "not_found"

class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Unauthorized."
    default_code = "unauthorized"

class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Forbidden."
    default_code = "forbidden"

class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict."
    default_code = "conflict"
