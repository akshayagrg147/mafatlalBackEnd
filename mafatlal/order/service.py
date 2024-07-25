from .models import TblOrder
from login.models import TblUser
from mafatlal import api_serializer
from home_screen.service import product_info_logic
import ast, datetime


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


def order_place_logic(data):
    try:
        final_response = []
        serializer = api_serializer.order_place_serializer(data=data)
        serializer.is_valid(raise_exception= True)
            
        products_list = []
        for products in data['products']:
            product_obj = {
                "product_id"    : products['product_id'],
                "size"          : products['size'],
                "quantity"      : products['quantity'],
                "price"         : products['price']
            }
            products_list.append(product_obj)
        
        TblOrder.objects.create(product_quantity = len(data['products']), user_id = data['user_id'], price = data['price'], order_details = products_list, delievery_address = data['address'], delievery_state = data['state'], delievery_pincode = data['pincode'], order_status='Pending', created_on = datetime.datetime.utcnow(), updated_on = datetime.datetime.utcnow(), created_by = data['user_id'])
        
        return True, final_response, "Order placed successfully"
        
    except ValueError as ve:
        print(f"Error at order placing api {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order placing api {str(e)}")
        return False, None, str(e)

def order_details_logic(order_id):
    try:
        final_response = {}
        if not order_id:
            print("Order id can't be null")
            raise ValueError("Order id can't be null")
        
        order_object = TblOrder.objects.filter(id = order_id).first()
        if not order_object:
            print("Can't find order with this id")
            raise ValueError("Can't find order with this id")
        
        product_details = []
        if order_object.order_details:
            for products in ast.literal_eval(order_object.order_details):
                product_info = {}
                status, response_data, message = product_info_logic(products['product_id'])
                print(f"Status and message for product id {products['product_id']} is {status} {message}")
                if response_data:
                    product_info['product_id']          = products['product_id']
                    product_info['size']                = products['size']
                    product_info['quantity']            = products['quantity']
                    product_info['price']               = products['price']
                    product_info['product_image']       = response_data['product_image']
                    product_info['product_name']        = response_data['name']
                    product_info['product_category']    = response_data['product_category']
                product_details.append(product_info)
        
        final_response['order_id']      = order_object.id
        final_response['user_id']       = order_object.user_id
        final_response['price']         = order_object.price
        final_response['products']      = product_details
        final_response['quantity']      = order_object.product_quantity
        final_response['order_status']  = order_object.order_status
        final_response['order_placed']  = order_object.created_on
        final_response['address']       = order_object.delievery_address
        final_response['state']         = order_object.delievery_state
        final_response['pincode']       = order_object.delievery_pincode
        
        return True, final_response, "Order placed successfully"
    
    except ValueError as ve:
        print(f"Error at order details api {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order details api {str(e)}")
        return False, None, str(e)
    