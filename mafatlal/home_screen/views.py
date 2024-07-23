from rest_framework.decorators import api_view
from mafatlal.response import JsendSuccessResponse
from mafatlal import constants
from .service import home_screen_logic, product_info_logic,sub_catproduct_info_logic, product_info_list_logic
import json

@api_view(['GET'])
def home_screen_info(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_HOME_SCREEN_API)
    
    data = request.query_params
    user_id = data['user_id'] if 'user_id' in data else None
    
    status, response_data, message = home_screen_logic(user_id)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['GET'])
def home_sub_category_product_info(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_SUBCAT_PRODUCT_API)
    
    data = request.query_params
    sub_cat_id = data['sub_id'] if 'sub_id' in data else None
    
    status, response_data, message = sub_catproduct_info_logic(sub_cat_id)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()

@api_view(['POST'])
def product_info_list(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_SUBCAT_PRODUCT_API)
    
    status = 'Error'
    response_data = None
    message = "Invalid params"
    data = request.body
    
    if data:
        data = data.decode("utf-8")
        
        data = json.loads(data)
    
    product_ids = data['ids'] if 'ids' in data else None
    
    if product_ids and isinstance(product_ids, list):
        status, response_data, message = product_info_list_logic(product_ids)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()


@api_view(['GET'])
def product_info(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_PRODUCT_INFO_API)
    
    data = request.query_params
    product_id = data['id'] if 'id' in data else None
    
    status, response_data, message = product_info_logic(product_id)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()
        
    