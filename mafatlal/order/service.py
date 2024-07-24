from .models import TblOrder
from login.models import TblUser

def order_history_logic(user_id):
    try:
        final_response = []
        if not user_id:
            print("User can't be none")
            raise ValueError("User can't be none")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise ValueError("No user found")
        
        orders_objs = TblOrder.objects.filter(user_id = user_id).all()
        
        for order in orders_objs:
            response = {
                "product_id": order.id,
                "product_quantity": order.product_quantity,
                "user_id": order.user_id,
                "price": order.price,
                "product_image": order.product_image,
                "description": order.description,
                "order_details": order.order_details,
                "order_status": order.order_status,
                "delievery_address": order.delievery_address,
                "delievery_state": order.delievery_state,
                "delievery_pincode": order.delievery_pincode,
                "created_on": order.created_on,
                "created_by": order.created_by,
                "updated_on": order.updated_on,
                "updated_by": order.updated_by
            }
            
            final_response.append(response)
        return True, final_response, "Order history fetch successfully"
        
    except ValueError as ve:
        print(f"Error at order history api {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order history api {str(e)}")
        return False, None, str(e)
        