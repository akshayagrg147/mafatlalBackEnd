from .models import TblOrder
from login.models import TblUser
from mafatlal import api_serializer
from home_screen.service import product_info_logic
from django.core import serializers as json_serializer
import ast, datetime, json


def order_history_logic(data):
    try:
        final_response = []
        user_id = data['user_id'] if 'user_id' in data else None
        if not user_id:
            print("User can't be none")
            raise ValueError("User can't be none")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise ValueError("No user found")
        
        orders_objs = TblOrder.objects.filter(user_id = user_id).all()
        
        for order in orders_objs:
            response = {
                "order_id"              : order.id,
                "product_quantity"      : order.product_quantity,
                "user_id"               : order.user_id,
                "price"                 : order.price,
                "product_image"         : order.product_image,
                "description"           : order.description,
                "order_status"          : order.order_status,
                "delievery_address"     : order.delievery_address,
                "delievery_state"       : order.delievery_state,
                "delievery_district"    : order.delievery_district,
                "delievery_city"        : order.delievery_city,
                "delievery_pincode"     : order.delievery_pincode,
                "created_on"            : order.created_on,
                "created_by"            : order.created_by,
                "updated_on"            : order.updated_on,
                "updated_by"            : order.updated_by,
                "tracking_url"          : order.tracking_url
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
        
        order_obj = TblOrder(product_quantity = len(data['products']), user_id = data['user_id'], price = data['price'], order_details = products_list, delievery_address = data['address'], delievery_state = data['state'], delievery_pincode = data['pincode'], order_status='Pending', created_on = datetime.datetime.now(datetime.timezone.utc), updated_on = datetime.datetime.now(datetime.timezone.utc), created_by = data['user_id'], delievery_district = data['district'], delievery_city = data['city'], product_image = data['image'] if 'image' in data else None, tracking_url = None)
        
        order_obj.save()
        order_obj = json_serializer.serialize('json', [order_obj])
        order_obj = json.loads(order_obj)
        
        response_obj = order_obj[0]['fields']
        return True, response_obj, "Order placed successfully"
        
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
        final_response['district']      = order_object.delievery_district
        final_response['city']          = order_object.delievery_city
        final_response['pincode']       = order_object.delievery_pincode
        final_response['tracking_url']  = order_object.tracking_url
        
        return True, final_response, "Order placed successfully"
    
    except ValueError as ve:
        print(f"Error at order details api {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order details api {str(e)}")
        return False, None, str(e)
     
def order_status_update_logic(data):
    try:
        order_id = data['order_id'] if 'order_id' in data else None
        if not order_id:
            print("Order id can't be null")
            raise ValueError("Order id can't be null")
        
        order_object = TblOrder.objects.filter(id = order_id).first()
        if not order_object:
            print("Can't find order with this id")
            raise ValueError("Can't find order with this id")
        
        permissioned_status = ['ordered', 'cancelled', 'dispatched']
        
        status = data['status'] if 'status' in data or data['status'] in permissioned_status else None
        
        if not status:
            raise ValueError("Error in order_status_update as status is not correct")
        
        order_object.order_status = status
        
        if status == 'dispatched':
            tracking_url = data['tracking_url'] if 'tracking_url' in data else None
            
            if not tracking_url:
                raise ValueError("Error in order_status_update as tracking url is not mentioned")
            
            order_object.tracking_url = tracking_url
            
        order_object.save()
        
        order_obj = json_serializer.serialize('json', [order_object])
        order_obj = json.loads(order_obj)
        
        response_obj = order_obj[0]['fields']
        return True, response_obj, "Order status updated successfully"
        
    except ValueError as ve:
        print(f"Error at order_status_update api {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order_status_update api {str(e)}")
        return False, None, str(e)
    
def order_list_logic(data):
    try:
        final_response = []
        user_id = data['user_id'] if 'user_id' in data else None
        if not user_id:
            print("User can't be none")
            raise ValueError("User can't be none")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise ValueError("No user found")
        
        page = data['page'] if 'page' in data else 1
        
        # If user_type is 1 then user is a distributor so 
        # we show all order of his state
        if user_obj.user_type == 2:
            from_date = data['from'] if 'from' in data else datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = data['to'] if 'to' in data else datetime.datetime.now(datetime.timezone.utc)
            
            order_status = data['status'] if 'status' in data else None
            
            if order_status:
                orders_objs = TblOrder.objects.filter(delievery_state = user_obj.state, created_on__gt = from_date, created_on__lt = to_date, order_status = order_status).all().order_by('created_on')
                
            else:
                orders_objs = TblOrder.objects.filter(delievery_state = user_obj.state, created_on__gt = from_date, created_on__lt = to_date).all().order_by('created_on')
            
        # if user_type is 0 then we show order of that user only
        else:
            orders_objs = TblOrder.objects.filter(user_id = user_id).all()
            
        total_orders = len(orders_objs)
        limit = 20*int(page) if 20*int(page) - total_orders < 0 else total_orders
        
        for flag in range(20*(int(page)-1), limit):
            customer_obj = TblUser.objects.filter(id = orders_objs[flag].user_id).first()
            response = {
                "order_id"              : orders_objs[flag].id,
                "created_on"            : orders_objs[flag].created_on,
                "customer_name"         : customer_obj.full_name,
                "product_quantity"      : orders_objs[flag].product_quantity,
                "user_id"               : orders_objs[flag].user_id,
                "channel"               : "Online Store",
                "price"                 : orders_objs[flag].price,
                "product_image"         : orders_objs[flag].product_image,
                "delievery_method"      : "Free Shipping" if float(orders_objs[flag].price) > 500 else "Standard Shipping",
                "description"           : orders_objs[flag].description,
                "order_status"          : orders_objs[flag].order_status,
                "delievery_address"     : orders_objs[flag].delievery_address,
                "delievery_state"       : orders_objs[flag].delievery_state,
                "delievery_district"    : orders_objs[flag].delievery_district,
                "delievery_city"        : orders_objs[flag].delievery_city,
                "delievery_pincode"     : orders_objs[flag].delievery_pincode,
                "created_by"            : orders_objs[flag].created_by,
                "updated_on"            : orders_objs[flag].updated_on,
                "updated_by"            : orders_objs[flag].updated_by,
                "tracking_url"          : orders_objs[flag].tracking_url
            }
            
            final_response.append(response)
        return True, final_response, "Order list fetch successfully"
        
    
    except ValueError as ve:
        print(f"Error at order list api {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order list api {str(e)}")
        return False, None, str(e)

