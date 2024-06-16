from typing import Any, Dict, Optional
from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer, ), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='inline_serializer', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def format_response(
    success: bool, 
    data: Optional[Any] = None, 
    message: Optional[str] = None, 
    error_code: Optional[int] = None, 
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    response = {
        'success': success,
        'data': data,
        'message': message,
        'error_code': error_code,
        'metadata': metadata
    }
    # Remove keys with None values for a cleaner response
    return {K:v for k, v in response.items() if v is not None}
