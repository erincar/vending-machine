from rest_framework.exceptions import APIException


class UsernameAlreadyExists(APIException):
    status_code = 409
    default_detail = "Username already exists."
    default_code = "username_exists"
