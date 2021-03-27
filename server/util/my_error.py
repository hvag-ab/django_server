from rest_framework import status
from rest_framework.exceptions import APIException


class ErrorCode:
    PARAM_ERROR = 498  # 参数验证错误
    DATA_NOT_FOUND = 497  # 未找到数据
    DATA_NOT_VALID = 496  # 数据错误
    LOGIN_FAIL = 499 # 登录失败


class ParseError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '这里是定义错误的描述'
    default_code = 'parse_error'
#
# ParseError(detail='错误描述',code=400)

class LoginFailError(APIException):
    status_code = ErrorCode.LOGIN_FAIL
    default_detail = '这里是定义错误的描述'
    default_code = 'parse_error'



