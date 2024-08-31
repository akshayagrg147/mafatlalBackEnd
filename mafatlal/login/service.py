from .models import TblUser, TblUserType
import hashlib
import hmac
from mafatlal.api_serializer import user_login_serializer, user_register_serializer
from mafatlal import constants
import random
from django.core import serializers as json_serializer
from datetime import datetime, timezone
import string
import json

def register_user(data):
    try:
        user_type_obj = None
        serializer = user_register_serializer(data=data)
        serializer.is_valid(raise_exception = True)
        
        user_obj = TblUser.objects.filter(email = data['email']).first()
        if user_obj:
            return True, None, 'User already registered'
        
        salt_key = generate_salt_key()
        
        encoded_password = hmac.new(salt_key.encode(), data['password'].encode(), hashlib.sha512).hexdigest()
        
        user_type = data['type'].lowercase() if 'type' in data else 'retailer'
        if user_type:
            user_type_obj = TblUserType.objects.filter(type_name = user_type.lower()).first()
        
        user_obj = TblUser( email = data['email'],
                            full_name = data['name'],
                            password   = encoded_password,
                            salt_key   = salt_key,
                            state      = data['state'],
                            district   = data['district'],
                            gst_number = data['gst'],
                            user_type  = user_type_obj.type_number if user_type_obj else 0,
                            created_on  = datetime.now(timezone.utc),
                            created_by  = 'SYSTEM',
                            updated_on  = datetime.now(timezone.utc),
                            updated_by= 'SYSTEM')
        user_obj.save()
        
        user_obj = TblUser.objects.filter(email=data['email']).first()
        
        response_obj = {
            "id"                : user_obj.id,
            "email"             : user_obj.email,
            "full_name"         : user_obj.full_name,
            "password"          : user_obj.password,
            "salt_key"          : user_obj.salt_key,
            "state"             : user_obj.state,
            "district"          : user_obj.district,
            "user_type"         : user_type_obj.type_number if user_type_obj else 0,
            "gst_number"        : user_obj.gst_number,
            "shipping"          : None,
            "billing"           : None,
            "created_on"        : user_obj.created_on,
            "updated_on"        : user_obj.updated_on,
            "updated_by"        : user_obj.updated_by,
            "updated_on"        : user_obj.updated_on,
        }
        if user_obj.shipping_address:
            response_obj['shipping'] = {
                                    "id"                : user_obj.shipping_address_id if user_obj.shipping_address else "",
                                    "landmark"          : user_obj.shipping_address.landmark if user_obj.shipping_address else "",
                                    "state"             : user_obj.shipping_address.state if user_obj.shipping_address else "",
                                    "district"          : user_obj.shipping_address.district if user_obj.shipping_address else "",
                                    "street_address_1"  : user_obj.shipping_address.street_address_1 if user_obj.shipping_address else "",
                                    "street_address_2"  : user_obj.shipping_address.street_address_2 if user_obj.shipping_address else "",
                                    "pincode"           : user_obj.shipping_address.pincode if user_obj.shipping_address else "",
                                    "city"              : user_obj.shipping_address.city if user_obj.shipping_address else "",
                                    "phone_number"      : user_obj.shipping_address.phone_number if user_obj.shipping_address else ""
                                        }
        if user_obj.billing_address:
            response_obj['billing'] = {
                                    "id"                : user_obj.billing_address_id if user_obj.billing_address else "",
                                    "landmark"          : user_obj.billing_address.landmark if user_obj.billing_address else "",
                                    "state"             : user_obj.billing_address.state if user_obj.billing_address else "",
                                    "district"          : user_obj.billing_address.district if user_obj.billing_address else "",
                                    "street_address_1"  : user_obj.billing_address.street_address_1 if user_obj.billing_address else "",
                                    "street_address_2"  : user_obj.billing_address.street_address_2 if user_obj.billing_address else "",
                                    "pincode"           : user_obj.billing_address.pincode if user_obj.billing_address else "",
                                    "city"              : user_obj.billing_address.city if user_obj.billing_address else "",
                                    "phone_number"      : user_obj.billing_address.phone_number if user_obj.billing_address else ""
                                    }
        
        return True, response_obj, 'success'
        
        
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the register user :- {str(e)} ##################")

        return False, None, str(e)

def login_check(data):
    try:
        serializer = user_login_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        user_obj = TblUser.objects.filter(email = data['email']).first()
        
        if not user_obj:
            return False, None, "Email is not registered! please register"
        
        user_salt_key = user_obj.salt_key
        
        encoded_password = hmac.new(user_salt_key.encode(), data['password'].encode(), hashlib.sha512).hexdigest()
        
        if user_obj.password == encoded_password:
            response_obj = {
                "id"                : user_obj.id,
                "email"             : user_obj.email,
                "full_name"         : user_obj.full_name,
                "password"          : user_obj.password,
                "salt_key"          : user_obj.salt_key,
                "state"             : user_obj.state,
                "district"          : user_obj.district,
                "gst_number"        : user_obj.gst_number,
                "shipping"          : None,
                "billing"           : None,
                "user_type"         : user_obj.user_type,
                "created_on"        : user_obj.created_on,
                "updated_on"        : user_obj.updated_on,
                "updated_by"        : user_obj.updated_by,
                "updated_on"        : user_obj.updated_on,
            }
            
            if user_obj.shipping_address:
                response_obj['shipping'] = {
                                        "id"                : user_obj.shipping_address_id if user_obj.shipping_address else "",
                                        "landmark"          : user_obj.shipping_address.landmark if user_obj.shipping_address else "",
                                        "state"             : user_obj.shipping_address.state if user_obj.shipping_address else "",
                                        "district"          : user_obj.shipping_address.district if user_obj.shipping_address else "",
                                        "street_address_1"  : user_obj.shipping_address.street_address_1 if user_obj.shipping_address else "",
                                        "street_address_2"  : user_obj.shipping_address.street_address_2 if user_obj.shipping_address else "",
                                        "pincode"           : user_obj.shipping_address.pincode if user_obj.shipping_address else "",
                                        "city"              : user_obj.shipping_address.city if user_obj.shipping_address else "",
                                        "phone_number"      : user_obj.shipping_address.phone_number if user_obj.shipping_address else ""
                                            }
            if user_obj.billing_address:
                response_obj['billing'] = {
                                        "id"                : user_obj.billing_address_id if user_obj.billing_address else "",
                                        "landmark"          : user_obj.billing_address.landmark if user_obj.billing_address else "",
                                        "state"             : user_obj.billing_address.state if user_obj.billing_address else "",
                                        "district"          : user_obj.billing_address.district if user_obj.billing_address else "",
                                        "street_address_1"  : user_obj.billing_address.street_address_1 if user_obj.billing_address else "",
                                        "street_address_2"  : user_obj.billing_address.street_address_2 if user_obj.billing_address else "",
                                        "pincode"           : user_obj.billing_address.pincode if user_obj.billing_address else "",
                                        "city"              : user_obj.billing_address.city if user_obj.billing_address else "",
                                        "phone_number"      : user_obj.billing_address.phone_number if user_obj.billing_address else ""
                                        }
            
            return True, response_obj, 'Success'
        
        else:
            return False, None, 'Invalid email/password'
    
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the login_check :- {str(e)} ##################")

        return False, None, str(e)
    
def generate_salt_key(length=10):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def user_info_logic(user_id):
    try:
        if not user_id:
            return 'Error', None, "User_id can't be null"
        
        user_obj = TblUser.objects.filter(id=user_id).first()
        
        response_obj = {
            "id"                : user_obj.id,
            "email"             : user_obj.email,
            "full_name"         : user_obj.full_name,
            "password"          : user_obj.password,
            "salt_key"          : user_obj.salt_key,
            "state"             : user_obj.state,
            "district"          : user_obj.district,
            "user_type"         : user_obj.user_type,
            "gst_number"        : user_obj.gst_number,
            "shipping"          : None,
            "billing"           : None,
            "created_on"        : user_obj.created_on,
            "updated_on"        : user_obj.updated_on,
            "updated_by"        : user_obj.updated_by,
            "updated_on"        : user_obj.updated_on,
        }
        if user_obj.shipping_address:
            response_obj['shipping'] = {
                                    "landmark"          : user_obj.shipping_address.landmark if user_obj.shipping_address else "",
                                    "state"             : user_obj.shipping_address.state if user_obj.shipping_address else "",
                                    "district"          : user_obj.shipping_address.district if user_obj.shipping_address else "",
                                    "street_address_1"  : user_obj.shipping_address.street_address_1 if user_obj.shipping_address else "",
                                    "street_address_2"  : user_obj.shipping_address.street_address_2 if user_obj.shipping_address else "",
                                    "pincode"           : user_obj.shipping_address.pincode if user_obj.shipping_address else "",
                                    "city"              : user_obj.shipping_address.city if user_obj.shipping_address else "",
                                    "phone_number"      : user_obj.shipping_address.phone_number if user_obj.shipping_address else ""
                                        }
        if user_obj.billing_address:
            response_obj['billing'] = {
                                    "landmark"          : user_obj.billing_address.landmark if user_obj.billing_address else "",
                                    "state"             : user_obj.billing_address.state if user_obj.billing_address else "",
                                    "district"          : user_obj.billing_address.district if user_obj.billing_address else "",
                                    "street_address_1"  : user_obj.billing_address.street_address_1 if user_obj.billing_address else "",
                                    "street_address_2"  : user_obj.billing_address.street_address_2 if user_obj.billing_address else "",
                                    "pincode"           : user_obj.billing_address.pincode if user_obj.billing_address else "",
                                    "city"              : user_obj.billing_address.city if user_obj.billing_address else "",
                                    "phone_number"      : user_obj.billing_address.phone_number if user_obj.billing_address else ""
                                    }
        
        return True, response_obj, 'success'
        
        
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the register user :- {str(e)} ##################")

        return False, None, str(e)