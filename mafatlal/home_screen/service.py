from home_screen.models import TblCategories, TblSubcategories, TblProducts
from mafatlal import constants
from login.models import TblUser
from django.db.models import F
from django.core import serializers as json_serializer
import json, ast


def home_screen_logic(user_id):
    try:
        final_response = {}
        user_obj = TblUser.objects.filter(id = user_id).first()
        
        if not user_obj:
            return False, None, "User not found"
        
        user_state = user_obj.state
        categories_info = {}
        
        all_categories = TblCategories.objects.filter(state = user_state).all()
        
        for categories in all_categories:
            categories_info[categories.categories_name] = handle_categories(categories)
            
        final_response['categories'] = categories_info
        
        products_info = handle_product_info()
        
        final_response['products'] = products_info
        
        return True, final_response, "All categories found successfully"
            
        
    except Exception as e:
        print(constants.BREAKCODE)
        print(f"!!! ERROR !!! Error with the home screen logic :- {str(e)} ##################")

        return False, None, str(e)
    
def handle_categories(categories):
    final_response = {}
    
    if not categories:
        return None
    
    sub_categories = TblSubcategories.objects.filter(category = categories.id).all()
    
    for category in sub_categories:
        final_response[category.subcategories_name] = category.id
    
    return final_response

def handle_product_info():
    final_response = []
    products_obj = TblProducts.objects.select_related('product_category').filter(
    product_category__categories_name='Global',
    product_category__state='Global'
    )
    
    if products_obj:
        for obj in products_obj:
            response = {}
            
            category = TblCategories.objects.filter(id = obj.__dict__['product_category_id']).first()
            size_dict = obj.__dict__['size_available']
            size_dict = json.dumps(size_dict)
            response = {
                "product_id"        : obj.__dict__['id'],
                "product_name"      : obj.__dict__['product_name'],
                "product_category"  : category.categories_name if category else 'Global',
                "size_available"    : json.loads(size_dict),
                "product_image"     : obj.__dict__['product_image'],
                "price"             : obj.__dict__['price']
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
        
        if product_obj:
            product_category = TblCategories.objects.filter(id = int(product_obj.product_category.id)).first()
            product_sub_category = TblSubcategories.objects.filter(id = int(product_obj.product_sub_category)).first()
            final_response['id']                        = product_id
            final_response['name']                      = product_obj.product_name
            final_response['product_category']          = product_category.categories_name
            final_response['product_sub_category']      = product_sub_category.subcategories_name
            final_response['size_available']            = product_obj.size_available
            final_response['product_image']             = product_obj.product_image
            final_response['price']                     = product_obj.price
            final_response['description']               = product_obj.description
            
        return True, final_response, 'Product data fetched successfully'
            
    except ValueError as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return False, None, str(e)
    
    except Exception as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return False, None, str(e)
    
def sub_catproduct_info_logic(sub_catid):
    try:
        final_response = []
        
        products_obj = TblProducts.objects.filter(product_sub_category = sub_catid).all()
        
        if products_obj:
            for obj in products_obj:
                response = {}
                
                product_sub_category = TblSubcategories.objects.filter(id = int(obj.product_sub_category)).first()
                
                category = TblCategories.objects.filter(id = obj.__dict__['product_category_id']).first()
                size_dict = obj.__dict__['size_available']
                size_dict = json.dumps(size_dict)
                response = {
                    "product_id"            : obj.__dict__['id'],
                    "product_name"          : obj.__dict__['product_name'],
                    "product_category"      : category.categories_name if category else 'Global',
                    "product_sub_category"  : product_sub_category.subcategories_name if product_sub_category else 'Global',
                    "size_available"        : json.loads(size_dict),
                    "product_image"         : obj.__dict__['product_image'],
                    "price"                 : obj.__dict__['price']
                }
                
                final_response.append(response)
            
        return True, final_response, 'Product data fetched successfully'
            
    except ValueError as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return False, None, str(e)
    
    except Exception as e:
        print(f"Error while extracting th procuct info as {str(e)}")
        return False, None, str(e)