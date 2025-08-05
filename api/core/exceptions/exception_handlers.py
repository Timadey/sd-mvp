from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail
from django.conf import settings
from rest_framework.response import Response
import traceback

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    errors = response.data if response and isinstance(response.data, dict) else {}

    def extract_messages(data):
        """
        Extracts the first message from each field to form a user-friendly summary.
        """
        error_message = []
        if isinstance(data, dict):
            for field, value in data.items():
                if isinstance(value, list) and value:
                    error_message.append(str(value[0]))
                elif isinstance(value, ErrorDetail):
                    error_message.append(str(value))
                elif isinstance(value, str):
                    error_message.append(value)
        return error_message

    # The main message is either from "detail" or a summary of the first few field errors
    if response and "detail" in response.data:
        message = str(response.data["detail"])
    else:
        messages = extract_messages(errors)

        if messages:
            message = (
                f"{messages[0]} And {len(messages) - 1} other error{'s' if len(messages) - 1 != 1 else ''}"
                if len(messages) > 1
                else messages[0]
            )
        else:
            message = "An error occurred while processing the request"

    payload = {
        "status": "error",
        "message": message,
        "errors": errors,
    }

    if settings.DEBUG:
        payload["trace"] = traceback.format_exc()

    return Response(payload, status=response.status_code if response else 500)
