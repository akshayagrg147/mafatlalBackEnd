from django.shortcuts import render
from rest_framework.decorators import api_view
from mafatlal.response import JsendSuccessResponse
from mafatlal import constants
from order.service import order_history_logic

# Create your views here.
@api_view(['GET'])
def order_history(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_HISTORY_API)
    
    data = request.query_params
    
    user_id = data['user_id'] if 'user_id' in data else None
    
    status, response_data, message = order_history_logic(user_id)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()