from django.shortcuts import render
from rest_framework.decorators import api_view
from mafatlal.response import JsendSuccessResponse
from .service import login_check, register_user
from mafatlal import constants

@api_view(['POST'])
def user_register(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_REGISTER_API)
    
    data = request.data
    status, response_data, message = register_user(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['POST'])
def user_login(request):
    print(constants.BREAKCODE)
    print(constants.INITIATED_LOGIN_API)

    data = request.data
    status, response_data, message = login_check(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()