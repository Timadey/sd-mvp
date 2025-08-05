from rest_framework.response import Response

def success(data=None, message="Your request was processed successfully", status=200):
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status)

def error(message="An error occurred while processing request", status=400, errors=None):
    return Response({
        "status": "error",
        "message": message,
        "errors": errors or []
    }, status=status)
