from rest_framework import status
from rest_framework.response import Response


class ResponseType:
    CREATED = 'created'
    RETRIEVED = 'resource-retrieved'
    INVALID = 'invalid'
    NOT_FOUND = 'not-found'
    UNAUTHORIZED = 'unauthorized'
    DESTROYED = 'destroyed'
    UPDATED = 'updated'


def ApiResponse(response_type, data=None, message=None):
    response_status = 'Resource Retrieved'
    response_status_code = status.HTTP_200_OK

    if response_type == ResponseType.UNAUTHORIZED:
        response_status = 'Unauthorized'
        response_status_code = status.HTTP_401_UNAUTHORIZED
    if response_type == ResponseType.NOT_FOUND:
        response_status = 'Not Found'
        response_status_code = status.HTTP_404_NOT_FOUND
    if response_type == ResponseType.INVALID:
        response_status = 'Invalid Input'
        response_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    if response_type == ResponseType.CREATED:
        response_status = 'Resource Created'
        response_status_code = status.HTTP_201_CREATED
    if response_type == ResponseType.DESTROYED:
        response_status = 'Resource Created'
        response_status_code = status.HTTP_200_OK
    if response_type == ResponseType.UPDATED:
        response_status = 'Resource Updated'
        response_status_code = status.HTTP_200_OK

    response_body = {
        "status": response_type,
        "message": message if message else response_status,
        "data": data
    }

    return Response(data=response_body, status=response_status_code)
