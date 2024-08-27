from .models import TblOrder
from login.models import TblUser
from home_screen.models import TblAddress
from mafatlal import api_serializer
from home_screen.service import product_info_logic
from django.core import serializers as json_serializer
import ast, datetime, json, math


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
                "description"           : order.description,
                "order_status"          : order.order_status,
                "shipping"              : None,
                "billing"               : None,
                "created_on"            : order.created_on,
                "created_by"            : order.created_by,
                "updated_on"            : order.updated_on,
                "updated_by"            : order.updated_by,
                "tracking_url"          : order.tracking_url
            }
            if order.shipping_address:
                response['shipping'] = {
                                        "landmark"  : order.shipping_address.landmark if order.shipping_address else "",
                                        "state"     : order.shipping_address.state if order.shipping_address else "",
                                        "district"  : order.shipping_address.district if order.shipping_address else "",
                                        "street_address_1"  : order.shipping_address.street_address_1 if order.shipping_address else "",
                                        "street_address_2"  : order.shipping_address.street_address_2 if order.shipping_address else "",
                                        "pincode"   : order.shipping_address.pincode if order.shipping_address else "",
                                        "city"      : order.shipping_address.city if order.shipping_address else ""
                                            }
            if order.billing_address:
                response['billing'] = {
                                        "landmark"  : order.billing_address.landmark if order.billing_address else "",
                                        "state"     : order.billing_address.state if order.billing_address else "",
                                        "district"  : order.billing_address.district if order.billing_address else "",
                                        "street_address_1"  : order.billing_address.street_address_1 if order.billing_address else "",
                                        "street_address_2"  : order.billing_address.street_address_2 if order.billing_address else "",
                                        "pincode"   : order.billing_address.pincode if order.billing_address else "",
                                        "city"      : order.billing_address.city if order.billing_address else ""
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
        
        shipping_obj    = None
        billing_obj     = None
            
        products_list = []
        for products in data['products']:
            product_obj = {
                "product_id"    : products['product_id'],
                "quantity"      : products['quantity'],
                "price"         : products['price']
            }
            if 'size' in products:
                product_obj["size"] = products['size']
                
            products_list.append(product_obj)
            
        shipping_address = data['shipping'] if 'shipping' in data else None
        billing_address = data['billing'] if 'billing' in data else None
        
        if shipping_address:
            if 'id' in shipping_address:
                shipping_obj = TblAddress.objects.filter(id = shipping_address['id'], user_id = data['user_id']).first()
                
            else:
                landmark        = shipping_address['landmark'] if 'landmark' in shipping_address else ''
                state           = shipping_address['state'] if 'state' in shipping_address else ''
                district        = shipping_address['district'] if 'district' in shipping_address else ''
                address_1       = shipping_address['street_address_1'] if 'street_address_1' in shipping_address else ''
                address_2       = shipping_address['street_address_2'] if 'street_address_2' in shipping_address else ''
                pincode         = shipping_address['pincode'] if 'pincode' in shipping_address else ''
                city            = shipping_address['city'] if 'city' in shipping_address else ''
                
                shipping_obj = TblAddress.objects.filter(user_id = data['user_id'], address_type = "shipping").first()
                
                if shipping_obj:
                    shipping_obj.landmark = landmark
                    shipping_obj.state = state
                    shipping_obj.district = district
                    shipping_obj.street_address_1 = address_1
                    shipping_obj.pincode = pincode
                    shipping_obj.city = city
                    shipping_obj.street_address_2 = address_2
                    
                    shipping_obj.save()
                
                else:
                    shipping_obj = TblAddress(user_id = data['user_id'], 
                                              address_type = "shipping",
                                              landmark = landmark,
                                              state = state,
                                              district = district,
                                              street_address_1 = address_1,
                                              pincode = pincode,
                                              city = city,
                                              street_address_2 = address_2)
                    
                    shipping_obj.save()
                    
                    shipping_obj = TblAddress.objects.filter(user_id = data['user_id'], address_type = "shipping").first()
                
        if billing_address:
            if 'id' in billing_address:
                billing_obj = TblAddress.objects.filter(id = billing_address['id'], user_id = data['user_id']).first()
                
            else:
                landmark        = billing_address['landmark'] if 'landmark' in billing_address else ''
                state           = billing_address['state'] if 'state' in billing_address else ''
                district        = billing_address['district'] if 'district' in billing_address else ''
                address_1       = billing_address['street_address_1'] if 'street_address_1' in billing_address else ''
                address_2       = billing_address['street_address_2'] if 'street_address_2' in billing_address else ''
                pincode         = billing_address['pincode'] if 'pincode' in billing_address else ''
                city            = billing_address['city'] if 'city' in billing_address else ''
                
                billing_obj = TblAddress.objects.filter(user_id = data['user_id'], address_type = "billing").first()
                
                if billing_obj:
                    billing_obj.landmark = landmark
                    billing_obj.state = state
                    billing_obj.district = district
                    billing_obj.street_address_1 = address_1
                    billing_obj.pincode = pincode
                    billing_obj.city = city
                    billing_obj.street_address_2 = address_2
                    
                    billing_obj.save()
                
                else:
                    billing_obj = TblAddress(user_id = data['user_id'], 
                                              address_type = "billing",
                                              landmark = landmark,
                                              state = state,
                                              district = district,
                                              street_address_1 = address_1,
                                              pincode = pincode,
                                              city = city,
                                              street_address_2 = address_2)
                    
                    billing_obj.save()
                    
                    billing_obj = TblAddress.objects.filter(user_id = data['user_id'], address_type = "billing").first()
                
        
        order_obj = TblOrder(product_quantity = len(data['products']), 
                             user_id = data['user_id'], 
                             price = data['price'], 
                             order_details = products_list,  
                             order_status='Pending', 
                             shipping_address = shipping_obj if shipping_obj else None,
                             billing_address = billing_obj if billing_obj else None,
                             created_on = datetime.datetime.now(datetime.timezone.utc), 
                             updated_on = datetime.datetime.now(datetime.timezone.utc), 
                             created_by = data['user_id'],
                             tracking_url = None)
        
        order_obj.save()
        response = {
                "order_id"              : order_obj.id,
                "product_quantity"      : order_obj.product_quantity,
                "user_id"               : order_obj.user_id,
                "price"                 : order_obj.price,
                "product_image"         : order_obj.product_image,
                "description"           : order_obj.description,
                "order_status"          : order_obj.order_status,
                "shipping"              : None,
                "billing"               : None,
                "created_on"            : order_obj.created_on,
                "created_by"            : order_obj.created_by,
                "updated_on"            : order_obj.updated_on,
                "updated_by"            : order_obj.updated_by,
                "tracking_url"          : order_obj.tracking_url
            }
        if order_obj.shipping_address:
            response['shipping'] = {
                                    "landmark"  : order_obj.shipping_address.landmark if order_obj.shipping_address else "",
                                    "state"     : order_obj.shipping_address.state if order_obj.shipping_address else "",
                                    "district"  : order_obj.shipping_address.district if order_obj.shipping_address else "",
                                    "street_address_1"  : order_obj.shipping_address.street_address_1 if order_obj.shipping_address else "",
                                    "street_address_2"  : order_obj.shipping_address.street_address_2 if order_obj.shipping_address else "",
                                    "pincode"   : order_obj.shipping_address.pincode if order_obj.shipping_address else "",
                                    "city"      : order_obj.shipping_address.city if order_obj.shipping_address else ""
                                        }
        if order_obj.billing_address:
            response['billing'] = {
                                    "landmark"  : order_obj.billing_address.landmark if order_obj.billing_address else "",
                                    "state"     : order_obj.billing_address.state if order_obj.billing_address else "",
                                    "district"  : order_obj.billing_address.district if order_obj.billing_address else "",
                                    "street_address_1"  : order_obj.billing_address.street_address_1 if order_obj.billing_address else "",
                                    "street_address_2"  : order_obj.billing_address.street_address_2 if order_obj.billing_address else "",
                                    "pincode"   : order_obj.billing_address.pincode if order_obj.billing_address else "",
                                    "city"      : order_obj.billing_address.city if order_obj.billing_address else ""
                                    }
        
        return True, response, "Order placed successfully"
        
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
                    product_info['quantity']            = products['quantity']
                    product_info['price']               = products['price']
                    product_info['product_image']       = response_data['product_image']
                    product_info['product_name']        = response_data['name']
                    product_info['product_category']    = response_data['product_category']
                    if 'size' in products:
                        product_info['size'] = products['size']
                product_details.append(product_info)
        
        final_response['shipping'] = None
        final_response['billing'] = None
                
        if order_object.shipping_address:
            final_response['shipping'] = {
                                    "landmark"          : order_object.shipping_address.landmark if order_object.shipping_address else "",
                                    "state"             : order_object.shipping_address.state if order_object.shipping_address else "",
                                    "district"          : order_object.shipping_address.district if order_object.shipping_address else "",
                                    "street_address_1"  : order_object.shipping_address.street_address_1 if order_object.shipping_address else "",
                                    "street_address_2"  : order_object.shipping_address.street_address_2 if order_object.shipping_address else "",
                                    "pincode"           : order_object.shipping_address.pincode if order_object.shipping_address else "",
                                    "city"              : order_object.shipping_address.city if order_object.shipping_address else ""
                                        }
        if order_object.billing_address:
            final_response['billing'] = {
                                    "landmark"          : order_object.billing_address.landmark if order_object.billing_address else "",
                                    "state"             : order_object.billing_address.state if order_object.billing_address else "",
                                    "district"          : order_object.billing_address.district if order_object.billing_address else "",
                                    "street_address_1"  : order_object.billing_address.street_address_1 if order_object.billing_address else "",
                                    "street_address_2"  : order_object.billing_address.street_address_2 if order_object.billing_address else "",
                                    "pincode"           : order_object.billing_address.pincode if order_object.billing_address else "",
                                    "city"              : order_object.billing_address.city if order_object.billing_address else ""
                                    }
        
        final_response['order_id']      = order_object.id
        final_response['user_id']       = order_object.user_id
        final_response['price']         = order_object.price
        final_response['products']      = product_details
        final_response['quantity']      = order_object.product_quantity
        final_response['order_status']  = order_object.order_status
        final_response['order_placed']  = order_object.created_on
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
        
        response = {
                "order_id"              : order_object.id,
                "product_quantity"      : order_object.product_quantity,
                "user_id"               : order_object.user_id,
                "price"                 : order_object.price,
                "description"           : order_object.description,
                "order_status"          : order_object.order_status,
                "shipping"              : None,
                "billing"               : None,
                "created_on"            : order_object.created_on,
                "created_by"            : order_object.created_by,
                "updated_on"            : order_object.updated_on,
                "updated_by"            : order_object.updated_by,
                "tracking_url"          : order_object.tracking_url
            }
        if order_object.shipping_address:
            response['shipping'] = {
                                    "landmark"  : order_object.shipping_address.landmark if order_object.shipping_address else "",
                                    "state"     : order_object.shipping_address.state if order_object.shipping_address else "",
                                    "district"  : order_object.shipping_address.district if order_object.shipping_address else "",
                                    "street_address_1"  : order_object.shipping_address.street_address_1 if order_object.shipping_address else "",
                                    "street_address_2"  : order_object.shipping_address.street_address_2 if order_object.shipping_address else "",
                                    "pincode"   : order_object.shipping_address.pincode if order_object.shipping_address else "",
                                    "city"      : order_object.shipping_address.city if order_object.shipping_address else ""
                                        }
        if order_object.billing_address:
            response['billing'] = {
                                    "landmark"  : order_object.billing_address.landmark if order_object.billing_address else "",
                                    "state"     : order_object.billing_address.state if order_object.billing_address else "",
                                    "district"  : order_object.billing_address.district if order_object.billing_address else "",
                                    "street_address_1"  : order_object.billing_address.street_address_1 if order_object.billing_address else "",
                                    "street_address_2"  : order_object.billing_address.street_address_2 if order_object.billing_address else "",
                                    "pincode"   : order_object.billing_address.pincode if order_object.billing_address else "",
                                    "city"      : order_object.billing_address.city if order_object.billing_address else ""
                                    }
        
        return True, response, "Order status updated successfully"
        
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
                orders_objs = TblOrder.objects.filter(
                    created_on__gt=from_date,
                    created_on__lt=to_date,
                    order_status = order_status
                ).order_by('-created_on')
                
            else:
                orders_objs = TblOrder.objects.filter(
                    created_on__gt=from_date,
                    created_on__lt=to_date
                ).order_by('-created_on')
            
        # if user_type is 0 then we show order of that user only
        else:
            orders_objs = TblOrder.objects.filter(user_id = user_id).all()
            
        total_orders = len(orders_objs)
        limit = 20*int(page) if 20*int(page) - total_orders < 0 else total_orders
        total_pages = math.ceil(total_orders/20)
        for flag in range(20*(int(page)-1), limit):
            customer_obj = TblUser.objects.filter(id = orders_objs[flag].user_id).first()
            response = {
                "order_id"              : orders_objs[flag].id,
                "created_on"            : orders_objs[flag].created_on,
                "customer_name"         : customer_obj.full_name if customer_obj else "",
                "product_quantity"      : orders_objs[flag].product_quantity,
                "user_id"               : orders_objs[flag].user_id,
                "channel"               : "Online Store",
                "price"                 : orders_objs[flag].price,
                "delievery_method"      : "Free Shipping" if float(orders_objs[flag].price) > 500 else "Standard Shipping",
                "description"           : orders_objs[flag].description,
                "order_status"          : orders_objs[flag].order_status,
                "shipping"              : None,
                "billing"               : None,
                "created_by"            : orders_objs[flag].created_by,
                "updated_on"            : orders_objs[flag].updated_on,
                "updated_by"            : orders_objs[flag].updated_by,
                "tracking_url"          : orders_objs[flag].tracking_url
            }
            
            if orders_objs[flag].shipping_address:
                response['shipping'] = {
                                        "landmark"          : orders_objs[flag].shipping_address.landmark if orders_objs[flag].shipping_address else "",
                                        "state"             : orders_objs[flag].shipping_address.state if orders_objs[flag].shipping_address else "",
                                        "district"          : orders_objs[flag].shipping_address.district if orders_objs[flag].shipping_address else "",
                                        "street_address_1"  : orders_objs[flag].shipping_address.street_address_1 if orders_objs[flag].shipping_address else "",
                                        "street_address_2"  : orders_objs[flag].shipping_address.street_address_2 if orders_objs[flag].shipping_address else "",
                                        "pincode"           : orders_objs[flag].shipping_address.pincode if orders_objs[flag].shipping_address else "",
                                        "city"              : orders_objs[flag].shipping_address.city if orders_objs[flag].shipping_address else ""
                                            }
            if orders_objs[flag].billing_address:
                response['billing'] = {
                                        "landmark"          : orders_objs[flag].billing_address.landmark if orders_objs[flag].billing_address else "",
                                        "state"             : orders_objs[flag].billing_address.state if orders_objs[flag].billing_address else "",
                                        "district"          : orders_objs[flag].billing_address.district if orders_objs[flag].billing_address else "",
                                        "street_address_1"  : orders_objs[flag].billing_address.street_address_1 if orders_objs[flag].billing_address else "",
                                        "street_address_2"  : orders_objs[flag].billing_address.street_address_2 if orders_objs[flag].billing_address else "",
                                        "pincode"           : orders_objs[flag].billing_address.pincode if orders_objs[flag].billing_address else "",
                                        "city"              : orders_objs[flag].billing_address.city if orders_objs[flag].billing_address else ""
                                        }
            
            final_response.append(response)
        return True, total_pages, final_response, "Order list fetch successfully"
        
    
    except ValueError as ve:
        print(f"Error at order list api {str(ve)}")
        return False, None,  None, str(ve)
    
    except Exception as e:
        print(f"Error at order list api {str(e)}")
        return False, None,  None, str(e)

def order_stats_logic(data):
    try:
        # Initialize totals
        total_profit = 0.0
        total_sale = 0.0

        # Extract user ID from data
        user_id = data.get('user_id')
        if not user_id:
            raise ValueError("User can't be none")
        
        # Fetch the user object
        user_obj = TblUser.objects.filter(id=user_id).first()
        if not user_obj:
            raise ValueError("No user found")
        
        # Extract or set default dates
        from_date = data.get('from', datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))
        to_date = data.get('to', datetime.datetime.now(datetime.timezone.utc))
        
        # Extract or set default order status
        order_status = data.get('status')
        
        # Filter the orders based on the status if provided
        filter_args = {
            'created_on__gt': from_date,
            'created_on__lt': to_date
        }
        
        if order_status:
            filter_args['order_status'] = order_status
        
        # Calculate total sale count    
        order_objs = TblOrder.objects.filter(**filter_args).all()

        # Calculate total profit
        statistics = {}
        for order in order_objs:
            date_key = order.created_on.strftime("%Y-%m-%d")
            
            total_profit += float(order.price)
            
            if date_key not in statistics:
                statistics[date_key] = []
            
            statistics[date_key].append({
                "orderId": order.id,
                "orderValue": order.price,
                "createdAt": order.created_on
            })
            
        
        total_sale = len(order_objs)
        total_profit = total_profit
            
        # Prepare the final response
        final_response = {
            "Total Sale": total_sale,
            "Total Profit": total_profit,
            "statistics": statistics
        }
        
        return True, final_response, "Order stats fetched successfully"
    
    except ValueError as ve:
        print(f"Error at order stats api: {str(ve)}")
        return False, None, str(ve)
    
    except Exception as e:
        print(f"Error at order stats api: {str(e)}")
        return False, None, str(e)
    




