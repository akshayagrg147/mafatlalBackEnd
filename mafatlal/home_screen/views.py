from rest_framework.decorators import api_view
from mafatlal.response import JsendSuccessResponse
from mafatlal import constants
from .service import home_screen_logic

@api_view(['GET'])
def home_screen_info(request):
    print(constants.BREAKCODE)
    print(constants.INITAITED_HOME_SCREEN_API)
    
    data = request.query_params
    user_id = data['user_id']
    
    status, response_data, message = home_screen_logic(user_id)
    
    return JsendSuccessResponse(status = status,data = response_data, message=message).get_response()