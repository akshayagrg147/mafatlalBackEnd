from django.shortcuts import render
from rest_framework.decorators import api_view
from mafatlal.response import JsendSuccessResponse
from mafatlal import constants
from order.service import order_history_logic, order_place_logic, order_details_logic, order_status_update_logic, order_list_logic, order_stats_logic, order_search_logic, verify_payment_logic, admin_order_list_logic, sales_overview_data_logic, order_status_wise_data_logic

# Create your views here.
@api_view(['GET'])
def order_history(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_HISTORY_API)
    
    data = request.query_params
    
    status, response_data, message = order_history_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def order_details(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_DETAILS_API)
    
    data = request.query_params
    
    order_id = data['order_id'] if 'order_id' in data else None
    
    status, response_data, message = order_details_logic(order_id)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['POST'])
def order_place(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_PLACE_ORDER_API)
    
    data = request.data
    
    status, response_data, message = order_place_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def order_status(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_STATS_API)
    
    data = request.query_params
    
    status, response_data, message = order_status_update_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def order_list(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_PLACE_LIST_API)
    
    data = request.query_params
    
    status, pages, response_data, message = order_list_logic(data)
    
    return JsendSuccessResponse(status = status, pages = pages, data = response_data, message=message).get_response()

@api_view(["GET"])
def order_stats(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_STATS_API)
    
    data = request.query_params
    
    status, response_data, message = order_stats_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def order_search(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_SEARCH_API)
    
    data = request.query_params
    
    status, response_data, message = order_search_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

    
@api_view(['POST'])
def verify_payment(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_VERIFY_PAYMENT_API)
    
    status, response_data, message = verify_payment_logic(request)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def admin_orders_details(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ADMIN_ORDER_LIST_API)
    
    data = request.query_params
    
    status, response_data, message = admin_order_list_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def sales_overview_logic(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_SALES_OVERVIEW_API)
    
    data = request.query_params
    
    status, response_data, message = sales_overview_data_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()


@api_view(['GET'])
def order_status_wise_logic(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_ORDER_STATUS_WISE_API)
    
    data = request.query_params
    
    status, response_data, message = order_status_wise_data_logic(data)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()
    
    




