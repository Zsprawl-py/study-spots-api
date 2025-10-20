from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response
    # normalize shape: {"detail": "...", "errors": {...}, "status": 400}
    data = {"status_code": response.status_code}
    if isinstance(response.data, dict):
        detail = response.data.get("detail")
        if detail is not None:
            data["detail"] = detail
        field_errors = {k: v for k, v in response.data.items() if k != "detail"}
        # field errors
        if field_errors:
            data["errors"] = field_errors
    else:
        data["detail"] = str(response.data)
    response.data = data
    return response
