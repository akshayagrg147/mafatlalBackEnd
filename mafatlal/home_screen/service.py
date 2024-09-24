from home_screen.models import TblCategories, TblSubcategories, TblProducts, TblAddress, TblDistrict, TblOrganization, TblState
from mafatlal import constants
from login.models import TblUser
from django.db.models import F
from mafatlal import api_serializer
from django.core import serializers as json_serializer
import json, ast


def home_screen_logic(user_id = None, category_id = None, flag = 'external'):
    try:
        final_response = {}
        # if flag == "external":
        #     if not user_id:
        #         return 'Error', None, "User_id can't be null"
            
        #     user_obj = TblUser.objects.filter(id = user_id).first()
            
        #     if not user_obj:
        #         return 'Error', None, "User not found"
        
        categories_info = []
        
        if category_id:
            all_categories = TblCategories.objects.filter(id = category_id).all()
        
        else:
            all_categories = TblCategories.objects.all()
        
        for categories in all_categories:
            category = {
                "id"            : categories.id,
                "name"          : categories.categories_name,
                "img"           : categories.image,
                "sub_categories": handle_sub_categories(categories.id)
            }
            
            categories_info.append(category)
            
            
        final_response['categories'] = categories_info
        
        products_info = handle_product_info()
        
        final_response['products'] = products_info
        
        return 'Success', final_response, "All categories found successfully"
            
        
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the home screen logic :- {str(e)} ##################")

        return 'Error', None, str(e)
    
def handle_sub_categories(cat_id=None):
    final_response = []
    
    if not cat_id:
        return None
    
    sub_categories = TblSubcategories.objects.filter(category = cat_id).all()
    
    for category in sub_categories:
        is_district = TblProducts.objects.filter(district__isnull=False, product_sub_category = category.id)
        is_state = TblProducts.objects.filter(state__isnull=False, product_sub_category = category.id)
        is_organization = TblProducts.objects.filter(organization__isnull=False, product_sub_category = category.id)
        respo = {
            "id"                : category.id,
            "name"              : category.subcategories_name,
            "img"               : category.image,
            "is_district"       : True if is_district else False,
            "is_state"          : True if is_state else False,
            "is_organization"   : True if is_organization else False
        }
        
        final_response.append(respo)
    
    return final_response

def handle_product_info():
    final_response = []
    products_obj = TblProducts.objects.select_related('product_category').filter(
    product_category__categories_name='Uniforms'
    )[:6]
    
    if products_obj:
        for obj in products_obj:
            response = {}
            
            category = TblCategories.objects.filter(id = obj.__dict__['product_category_id']).first()
            size_dict = obj.__dict__['size_available']
            size_dict = json.dumps(size_dict)
            images_list = ast.literal_eval(obj.__dict__['product_image'])
            products_images = {}
            for i in range(len(images_list)):
                products_images[f"image_{i+1}"] = images_list[i]
            response = {
                "product_id"            : obj.__dict__['id'],
                "Selected_category_id"  : category.id,
                "product_name"          : obj.__dict__['product_name'],
                "product_category"      : category.categories_name if category else 'Global',
                "size_available"        : json.loads(size_dict),
                "product_image"         : products_images,
                "price"                 : obj.__dict__['price']
            }
            
            final_response.append(response)
        
        return final_response
    else:
        return []
    
    
def product_info_logic(product_id):
    try:
        final_response = {}
        
        if not product_id:
            raise ValueError("Product id can't be null")
        
        product_obj = TblProducts.objects.filter(id = int(product_id)).first()
        
        related_products_objs = TblProducts.objects.filter(product_sub_category_id = product_obj.product_sub_category_id).all()
        related_products = []
        for objs in related_products_objs:
            product_category = TblCategories.objects.filter(id = int(objs.product_category_id)).first()
            product_sub_category = TblSubcategories.objects.filter(id = int(objs.product_sub_category_id)).first()
            images_list = ast.literal_eval(objs.__dict__['product_image'])
            products_images = {}
            for i in range(len(images_list)):
                products_images[f"image_{i+1}"] = images_list[i]
            related_products.append({
                'id'                        : objs.id,
                'name'                      : objs.product_name,
                'product_category_id'       : objs.product_category_id,
                'product_category'          : product_category.categories_name,
                'product_sub_category_id'   : objs.product_sub_category_id,
                'product_sub_category'      : product_category.categories_name,
                'size_available'            : product_sub_category.subcategories_name,
                'product_image'             : products_images,
                'price'                     : objs.price,
                'description'               : objs.description
            })
        
        if product_obj:
            images_list = ast.literal_eval(product_obj.product_image)
            products_images = {}
            for i in range(len(images_list)):
                products_images[f"image_{i+1}"] = images_list[i]
            product_category = TblCategories.objects.filter(id = int(product_obj.product_category_id)).first()
            product_sub_category = TblSubcategories.objects.filter(id = int(product_obj.product_sub_category_id)).first()
            final_response['id']                        = product_id
            final_response['name']                      = product_obj.product_name
            final_response['product_category']          = product_category.categories_name
            final_response['product_sub_category']      = product_sub_category.subcategories_name
            final_response['size_available']            = product_obj.size_available
            final_response['product_image']             = products_images
            final_response['price']                     = product_obj.price
            final_response['description']               = product_obj.description
            final_response['related_products']          = related_products
            
        return 'Success', final_response, 'Product data fetched successfully'
            
    except ValueError as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return 'Error', None, str(e)
    
    except Exception as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return 'Error', None, str(e)
    
def sub_catproduct_info_logic(data):
    try:
        final_response = []
        category_id = data['category'] if 'category' in data else None
        if category_id:
            return home_screen_logic(category_id=category_id, flag='internal')
        
        sub_catid = data['sub_id'] if 'sub_id' in data else None
        
        district_id = data['district'] if 'district' in data else None
        state_id = data['state'] if 'state' in data else None
        org_id = data['organization'] if 'organization' in data else None
        
        if district_id or state_id or org_id:
            if district_id:
                products_obj = TblProducts.objects.filter(district = district_id, product_sub_category = sub_catid).all()
            
            elif state_id:
                products_obj = TblProducts.objects.filter(state = state_id, product_sub_category = sub_catid).all()
            
            elif org_id:
                products_obj = TblProducts.objects.filter(organization = org_id, product_sub_category = sub_catid).all()
            
            if products_obj:
                for obj in products_obj:
                    response = {}
                    
                    product_sub_category = TblSubcategories.objects.filter(id = int(obj.product_sub_category_id)).first()
                    
                    category = TblCategories.objects.filter(id = obj.__dict__['product_category_id']).first()
                    size_dict = obj.__dict__['size_available']
                    size_dict = json.dumps(size_dict)
                    images_list = ast.literal_eval(obj.__dict__['product_image'])
                    products_images = {}
                    for i in range(len(images_list)):
                        products_images[f"image_{i+1}"] = images_list[i]
                    response = {
                        "product_id"            : obj.__dict__['id'],
                        "product_name"          : obj.__dict__['product_name'],
                        "product_category"      : category.categories_name if category else 'Global',
                        "product_sub_category"  : product_sub_category.subcategories_name if product_sub_category else 'Global',
                        "size_available"        : json.loads(size_dict),
                        "product_image"         : products_images,
                        "price"                 : obj.__dict__['price'],
                    }
                    
                    if obj.__dict__['district_id']:
                        response['district_id'] = obj.__dict__['district_id']
                        response['district_name'] = obj.district.district_name
                        response['state_id'] = obj.district.state_id
                        response['state_name'] = obj.district.state.state_name
                    
                    if obj.__dict__['state_id']:
                        response['state_id'] = obj.__dict__['state_id']
                        response['state_name'] = obj.state.state_name
                        
                    if obj.__dict__['organization_id']:
                        response['organization_id'] = obj.__dict__['organization_id']
                        response['organization_name'] = obj.organization.org_name
                        response['district_id'] = obj.organization.district_id
                        response['district_name'] = obj.organization.district.district_name
                        response['state_id'] = obj.organization.state_id
                        response['state_name'] = obj.organization.state.state_name
                    
                    final_response.append(response)
            
        else:
            products_obj = TblProducts.objects.filter(product_sub_category = sub_catid).all()
            
            if products_obj:
                for obj in products_obj:
                    response = {}
                    
                    product_sub_category = TblSubcategories.objects.filter(id = int(obj.product_sub_category_id)).first()
                    
                    category = TblCategories.objects.filter(id = obj.__dict__['product_category_id']).first()
                    size_dict = obj.__dict__['size_available']
                    size_dict = json.dumps(size_dict)
                    images_list = ast.literal_eval(obj.__dict__['product_image'])
                    products_images = {}
                    for i in range(len(images_list)):
                        products_images[f"image_{i+1}"] = images_list[i]
                    response = {
                        "product_id"            : obj.__dict__['id'],
                        "product_name"          : obj.__dict__['product_name'],
                        "product_category"      : category.categories_name if category else 'Global',
                        "product_sub_category"  : product_sub_category.subcategories_name if product_sub_category else 'Global',
                        "size_available"        : json.loads(size_dict),
                        "product_image"         : products_images,
                        "price"                 : obj.__dict__['price']
                    }
                    
                    final_response.append(response)
            
        return 'Success', final_response, 'Product data fetched successfully'
            
    except ValueError as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return 'Error', None, str(e)
    
    except Exception as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return 'Error', None, str(e)
    
def product_info_list_logic(product_ids):
    try:
        final_response = []
        for id in product_ids:
            status, response_data, message = product_info_logic(id)
            print(f"Status and message for product id {id} is {status} {message}")
            if response_data:
                final_response.append(response_data)
                
        return 'Success', final_response, 'Product data list fetched successfully'
        
    except ValueError as e:
        print(f"Error while extracting th procuct info list as {str(e)}")
        return 'Error', None, str(e)
    
    except Exception as e:
        print(f"Error while extracting th procuct info list as {str(e)}")
        return 'Error', None, str(e)
    
def address_insertion_logic(data):
    try:
        response_obj = {}
        user_id = int(data['user_id']) if 'user_id' in data else None
        
        if not user_id:
            print("Error in address_insertion_logic as User_id is null")
            raise ValueError("User_id is null")
        
        for key, value in data.items():
            if key != "user_id":
                address_type    = key
                landmark        = value['landmark'] if 'landmark' in value else ''
                state           = value['state'] if 'state' in value else ''
                district        = value['district'] if 'district' in value else ''
                address_1       = value['street_address_1'] if 'street_address_1' in value else ''
                address_2       = value['street_address_2'] if 'street_address_2' in value else ''
                pincode         = value['pincode'] if 'pincode' in value else ''
                city            = value['city'] if 'city' in value else ''
                phone_number    = value['phone_number'] if 'phone_number' in value else ''

                address_obj = TblAddress.objects.filter(user_id = user_id,address_type = address_type).first()
                if address_obj:
                    address_obj.address_type        = address_type if address_type else address_obj.address_type
                    address_obj.landmark            = landmark if landmark else address_obj.landmark
                    address_obj.state               = state if state else address_obj.state
                    address_obj.district            = district if district else address_obj.district
                    address_obj.street_address_1    = address_1 if address_1 else address_obj.street_address_1
                    address_obj.street_address_2    = address_2 if address_2 else address_obj.street_address_2
                    address_obj.pincode             = pincode if pincode else address_obj.pincode
                    address_obj.city                = city if city else address_obj.city
                    address_obj.phone_number        = phone_number if phone_number else address_obj.phone_number

                    address_obj.save()
                    
                else:
                    address_data = TblAddress(user_id = user_id,
                                            address_type = address_type,
                                            landmark = landmark,
                                            state = state,
                                            district = district,
                                            street_address_1 = address_1,
                                            street_address_2 = address_2,
                                            pincode = pincode, 
                                            city = city,
                                            phone_number = phone_number)
                    
                    address_data.save()
                
                    address_obj = TblAddress.objects.filter(user_id = user_id, address_type = address_type).first()
                
                response_obj[f'{address_type}_id']                  = address_obj.id
                response_obj[f'{address_type}_landmark']            = address_obj.landmark
                response_obj[f'{address_type}_street_address_1']    = address_obj.street_address_1
                response_obj[f'{address_type}_street_address_2']    = address_obj.street_address_2
                response_obj[f'{address_type}_state']               = address_obj.state
                response_obj[f'{address_type}_district']            = address_obj.district
                response_obj[f'{address_type}_pincode']             = address_obj.pincode
                response_obj[f'{address_type}_city']                = address_obj.city
                response_obj[f'{address_type}_phone_number']        = address_obj.phone_number
                
                user_obj = TblUser.objects.filter(id = user_id).first()
                if address_type == 'billing':
                    user_obj.billing_address = address_obj
                    user_obj.save()
                else:
                    user_obj.shipping_address = address_obj
                    user_obj.save()
        
        return 'Success', response_obj, 'Address Added successfully'
    
    except ValueError as e:
        print(f"Error in the address_insertion_logic as {str(e)}")
        return 'Error', None, str(e)
    
    except Exception as e:
        print(f"Error in the address_insertion_logic as {str(e)}")
        return 'Error', None, str(e)
    
def address_updation_logic(data):
    try:
        serializer = api_serializer.address_update_serializer(data=data)
        serializer.is_valid(raise_exception= True)
        
        address_id = int(data['address_id']) if 'address_id' in data else None
        address_type = data['address_type'] if 'address_type' in data else 'billing'
        
        address_obj = TblAddress.objects.filter(id = address_id).first()
        
        if address_obj:
            for key, value in data.items():
                if hasattr(address_obj, key):
                    setattr(address_obj, key, value)
                address_obj.save()
            
        else:
            raise ValueError("Address not found")
        
        address_data = TblAddress.objects.filter(id = address_id, address_type = address_type).first()
        address_type = address_data.address_type
        response_obj = {
            "id"                                : address_data.id,
            "address_type"                      : address_data.address_type,
            f"{address_type}_landmark"          : address_data.landmark,
            f"{address_type}_state"             : address_data.state,
            f"{address_type}_district"          : address_data.district,
            f"{address_type}_street_address_1"  : address_data.street_address_1,
            f"{address_type}_street_address_2"  : address_data.street_address_2,
            f"{address_type}_pincode"           : address_data.pincode,
            f"{address_type}_city"              : address_data.city,
            f"{address_type}_phone_number"      : address_data.phone_number,
        }
        
        return 'Success', response_obj, 'Address Updated successfully'
    
    except ValueError as e:
        print(f"Error in the address_insertion_logic as {str(e)}")
        return 'Error', None, str(e)
    
    except Exception as e:
        print(f"Error in the address_insertion_logic as {str(e)}")
        return 'Error', None, str(e)
    
def search_category_logic(data):
    try:
        final_response = {}
        categories_info = [] 
        
        search_string = data['search'] if 'search' in data else None
        
        if not search_string:
            raise Exception("Search string can't be null")
        
        
        all_categories = TblCategories.objects.filter(categories_name__icontains=search_string).all()
        
        for categories in all_categories:
            category = {
                "id"            : categories.id,
                "name"          : categories.categories_name,
                "img"           : categories.image,
                "sub_categories": handle_sub_categories(categories.id)
            }
            
            categories_info.append(category)
            
            
        final_response['categories'] = categories_info
        
        products_info = handle_product_info()
        
        final_response['products'] = products_info
        
        return 'Success', final_response, "All categories found successfully"
            
        
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the search_category_logicc :- {str(e)} ##################")

        return 'Error', None, str(e)
    
    
def get_states(data):
    try:
        final_response = []
        
        states_objs = TblState.objects.all()
        
        if states_objs:
            for obj in states_objs:
                final_response.append({'id' : obj.id, 'name' : obj.state_name})
                
        return 'Success', final_response, "All states found successfully"

    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the get_states :- {str(e)} ##################")

        return 'Error', None, str(e)


def get_district(data):
    try:
        final_response = []
        
        search_string = data['state'] if 'state' in data else None
        
        district_objs = TblDistrict.objects.filter(state_id =search_string).all()
        
        if district_objs:
            for obj in district_objs:
                final_response.append({'id' : obj.id, 'name' : obj.district_name, 'state_id' : obj.state_id, "state_name" : obj.state.state_name})
                
        return 'Success', final_response, "All categories found successfully"

    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the get_district :- {str(e)} ##################")

        return 'Error', None, str(e)


def get_organizations(data):
    try:
        final_response = []
        
        state_id = data['state'] if 'state' in data else None
        district_id = data['district'] if 'district' in data else None
        
        if state_id and district_id:
            products_objs = TblOrganization.objects.filter(state_id = state_id, district_id = district_id).all()
        
        elif state_id:
            products_objs = TblOrganization.objects.filter(state_id = state_id).all()
        
        elif district_id:
            products_objs = TblOrganization.objects.filter(district_id = district_id).all()
        if products_objs:
            for obj in products_objs:
                final_response.append({'id' : obj.id, 'name' : obj.org_name, 'state_id' : obj.state_id, "state_name" : obj.state.state_name, 'district_id' : obj.district_id, "district_name" : obj.district.district_name})
                
        return 'Success', final_response, "All organizations found successfully"

    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the get_organizations :- {str(e)} ##################")

        return 'Error', None, str(e)


    
    
    