from .models import TblUser
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
        serializer = user_register_serializer(data=data)
        serializer.is_valid(raise_exception = True)
        
        salt_key = generate_salt_key()
        
        encoded_password = hmac.new(salt_key.encode(), data['password'].encode(), hashlib.sha512).hexdigest()
        
        user_obj = TblUser( email = data['email'],
                            first_name = data['first_name'],
                            last_name  = data['last_name'],
                            password   = encoded_password,
                            salt_key   = salt_key,
                            is_distributor = False,
                            created_on  = datetime.now(timezone.utc),
                            created_by  = 'SYSTEM',
                            updated_on  = datetime.now(timezone.utc),
                            updated_by= 'SYSTEM')
        user_obj.save()
        
        user_obj = json_serializer.serialize('json', [user_obj])
        user_obj = json.loads(user_obj)
        
        response_obj = user_obj[0]['fields']
        
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
        
        user_salt_key = user_obj.salt_key
        
        encoded_password = hmac.new(user_salt_key.encode(), data['password'].encode(), hashlib.sha512).hexdigest()
        
        if user_obj.password == encoded_password:
            response = {
                "email"             : user_obj.email, 
                "first_name"        : user_obj.first_name,
                "last_name"         : user_obj.last_name,
                "is_distributor"    : user_obj.is_distributor,
            }
            
            return True, response, 'Success'
        
        else:
            return False, None, 'Invalid email/password'
    
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the login_check :- {str(e)} ##################")

        return False, None, str(e)
    
def generate_salt_key(length=10):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))