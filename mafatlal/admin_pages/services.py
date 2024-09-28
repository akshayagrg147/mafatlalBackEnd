from .models import TblCategories, TblSubcategories, TblProducts, TblOrganization, TblState, TblDistrict
from mafatlal.api_serializer import add_products_serializer
import datetime
from login.models import TblUser
import json
from django.db.models import Q
import ast
from dateutil.tz import gettz

# Categories Related Functions
def get_category(user_id):
    try:
        final_response = []
        if not user_id:
            raise Exception("User is null")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise Exception("User is not present")
        
        categories = TblCategories.objects.all()
        
        for cat_object in categories:
            response = {
                        "id"    : cat_object.id,
                        "name"  : cat_object.categories_name,
                        "image" : cat_object.image
                        }
            
            final_response.append(response)
            
        
        return True, final_response, "Categories fetched successully"
        
        
    except Exception as e:
        print(f"Error in fetching categories from database as {str(e)}")
        return False, {}, str(e)

def add_category(user_id, data):
    try:
        final_response = []
        message = []
        
        for obj in data:
            category_name = obj.get('name')
            category_image = obj.get('image')
            
            try:
                if category_name and category_image:
                    cat_object = TblCategories.objects.filter(categories_name = category_name, created_by = user_id).first()
                    
                    if cat_object:
                        cat_object.categories_name = category_name
                        cat_object.image = category_image
                        cat_object.updated_by = user_id
                        cat_object.save()
                        
                        response = {
                            "id"    : cat_object.id,
                            "name"  : cat_object.categories_name,
                            "image" : cat_object.image
                        }
                        
                        final_response.append(response)
                    
                    else:
                        category_object = TblCategories(categories_name = category_name,
                                                        image = category_image,
                                                        created_by = user_id)
                    
                        category_object.save()
                        
                        cat_object = TblCategories.objects.filter(categories_name = category_name, created_by = user_id).first()
                        
                        response = {
                            "id"    : cat_object.id,
                            "name"  : cat_object.categories_name,
                            "image" : cat_object.image
                        }
                        
                        final_response.append(response)
            
            except Exception as e:
                err_message = f"Error while adding category :- {category_name} as {str(e)}"
                message.append(err_message)
                
        if message:
            return True, final_response, message
        
        else:
            return True, final_response, "Organization Added successfully"
                
    except Exception as e:
        print(f"Error in adding organization in database as {str(e)}")
        return False, {}, str(e)
    
def update_category(data):
    try:
        category_id = data.get("id")
        
        if not category_id:
            raise Exception("Category id is none")
        
        category_object = TblCategories.objects.filter(id = category_id).first()
        
        if not category_object:
            raise Exception("Category not found")
        
        for key, value in data.items():
            if key == "name":
                category_object.categories_name = value
            if key == "image":
                category_object.image = value
                
            category_object.save()
            
        category_object.updated_by = data.get('user_id')
        category_object.save()
        
        response = {
                    "id"    : category_object.id,
                    "name"  : category_object.categories_name,
                    "image" : category_object.image
                }
        
        return True, response, "Category updated successfully"
        
    except Exception as e:
        print(f"Error in updating organization in database as {str(e)}")
        return False, {}, str(e)
    
def delete_category(data):
    try:
        category_id = data.get("id")
        
        if not category_id:
            raise Exception("Category id is none")
        
        global_cat_obj = TblCategories.objects.filter(categories_name = "Global").first()
        global_sub_obj = TblSubcategories.objects.filter(subcategories_name = "Global").first()
        
        category_object = TblCategories.objects.filter(id = category_id).first()
        
        if not category_object:
            raise Exception("Category not found")
        
        sub_categories = TblSubcategories.objects.filter(category=category_id)

        for sub_obj in sub_categories:
            TblProducts.objects.filter(product_sub_category=sub_obj.id).update(product_sub_category=global_sub_obj, product_category = global_cat_obj)
        
        for sub_cat in sub_categories:
            TblOrganization.objects.filter(sub=sub_cat.id).update(sub=global_sub_obj)

        # Delete subcategories and then the category
        sub_categories.delete()
        category_object.delete()
                
        return True, {}, "Category deleted successfully"
        
    except Exception as e:
        print(f"Error in updating organization in database as {str(e)}")
        return False, {}, str(e)


# Sub_categories Related Functions
def get_sub_category(data):
    try:
        final_response = []
        user_id = data.get('user_id')
        if not user_id:
            raise Exception("User is null")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise Exception("User is not present")
        
        category = data.get('category')
        if category:
            sub_category_obj = TblSubcategories.objects.filter(category = category).all()
        
        else:
            sub_category_obj = TblSubcategories.objects.all()
        
        for sub_obj in sub_category_obj:
            response = {
                        "id"                : sub_obj.id,
                        "name"              : sub_obj.subcategories_name,
                        "image"             : sub_obj.image,
                        "organization_id"   : sub_obj.category_id,
                        "organization_name" : sub_obj.category.categories_name
                    }
            
            final_response.append(response)
            
        
        return True, final_response, "Sub_category fetched successully"
        
        
    except Exception as e:
        print(f"Error in fetching sub_category from database as {str(e)}")
        return False, {}, str(e)

def add_sub_category(user_id, data):
    try:
        final_response = []
        message = []
        
        for obj in data:
            parent_category = int(obj.get('category'))
            sub_category_name = obj.get('name')
            sub_category_image = obj.get('image')
            
            try:
                if parent_category and sub_category_name and sub_category_image:
                    subcat_object = TblSubcategories.objects.filter(subcategories_name = sub_category_name, created_by = user_id, category = parent_category).first()
                    
                    if subcat_object:
                        subcat_object.subcategories_name = sub_category_name
                        subcat_object.image = sub_category_image
                        subcat_object.updated_by = user_id
                        subcat_object.save()
                        
                        response = {
                            "id"                : subcat_object.id,
                            "name"              : subcat_object.subcategories_name,
                            "image"             : subcat_object.image,
                            "category_id"       : subcat_object.category,
                            "category_name"     : subcat_object.category.categories_name
                        }
                        
                        final_response.append(response)
                    
                    else:
                        organization_object = TblCategories.objects.filter(id = parent_category).first()
                        if organization_object:
                            sub_category_object = TblSubcategories(subcategories_name = sub_category_name,
                                                                category = organization_object,
                                                                image = sub_category_image,
                                                                created_by = user_id)
                    
                            sub_category_object.save()
                        
                            subcat_object = TblSubcategories.objects.filter(subcategories_name = sub_category_name, created_by = user_id, category = parent_category).first()
                            
                            response = {
                                "id"                : subcat_object.id,
                                "name"              : subcat_object.subcategories_name,
                                "image"             : subcat_object.image,
                                "category_id"       : subcat_object.category_id,
                                "category_name"     : subcat_object.category.categories_name
                            }
                            
                            final_response.append(response)
                        
                        else:
                            raise Exception(f"{parent_category} category not found")
            
            except Exception as e:
                err_message = f"Error while adding sub_category :- {sub_category_image} as {str(e)}"
                message.append(err_message)
                
            if message:
                return True, final_response, message
            
            else:
                return True, final_response, "Sub_catogory Added successfully"
                
    except Exception as e:
        print(f"Error in adding Sub_catogory in database as {str(e)}")
        return False, {}, str(e)

def update_sub_category(data):
    try:
        sub_category_id = data.get("id")
        
        if not sub_category_id:
            raise Exception("Category id is none")
        
        subcategory_object = TblSubcategories.objects.filter(id = sub_category_id).first()
        
        if not subcategory_object:
            raise Exception("Category not found")
        
        for key, value in data.items():
            if key == "name":
                subcategory_object.subcategories_name = value
            if key == "image":
                subcategory_object.image = value
                
            subcategory_object.save()
            
        subcategory_object.updated_by = data.get('user_id')
        subcategory_object.save()
        
        response = {
                    "id"                : subcategory_object.id,
                    "name"              : subcategory_object.subcategories_name,
                    "image"             : subcategory_object.image,
                    "category_id"       : subcategory_object.category_id,
                    "category_name"     : subcategory_object.category.categories_name
                }
        
        return True, response, "sub_category updated successfully"
        
    except Exception as e:
        print(f"Error in updating sub_category in database as {str(e)}")
        return False, {}, str(e)

def delete_sub_category(data):
    try:
        subcat_id = data.get("id")
        
        if not subcat_id:
            raise Exception("sub_category id is none")
        
        global_sub_obj = TblSubcategories.objects.filter(subcategories_name = 'Global').first()
        
        sub_categories = TblSubcategories.objects.filter(id=subcat_id).first()

        if not sub_categories:
            raise Exception("sub_categories not found")
        
        TblProducts.objects.filter(product_sub_category=subcat_id).update(product_sub_category=global_sub_obj)
        TblOrganization.objects.filter(sub=subcat_id).update(sub=global_sub_obj)

        # Delete subcategories and then the category
        sub_categories.delete()
                
        return True, {}, "Sub_category deleted successfully"
        
    except Exception as e:
        print(f"Error in deleting sub_category from database as {str(e)}")
        return False, {}, str(e)


# Organization Related Functions
def get_orgs(data):
    try:
        final_response = []
        user_id = data.get('user_id')
        if not user_id:
            raise Exception("User is null")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise Exception("User is not present")
        
        sub_category = data.get('sub_category')
        if sub_category:
            organization_obj = TblOrganization.objects.filter(sub = sub_category).all()
        
        else:
            organization_obj = TblOrganization.objects.all()
        
        for orgs in organization_obj:
            response = {
                        "id"                : orgs.id,
                        "name"              : orgs.org_name,
                        "state_id"          : orgs.state.id,
                        "state"             : orgs.state.state_name,
                        "district_id"       : orgs.district.id,
                        "district"          : orgs.district.district_name,
                        "category_id"       : orgs.sub.category.id,
                        "category_name"     : orgs.sub.category.categories_name,
                        "sub_category_id"   : orgs.sub.id,
                        "sub_category_name" : orgs.sub.subcategories_name
                    }
            
            final_response.append(response)
            
        
        return True, final_response, "Organizations fetched successully"
        
        
    except Exception as e:
        print(f"Error in fetching organizations from database as {str(e)}")
        return False, {}, str(e)

# TODO to add the functionality for state and district if they are not present in db
def add_orgs(data):
    try:
        final_response = []
        message = []
        
        if data:
            for obj in data:
                parent_subcategory = int(obj.get('sub_category'))
                organization_name = obj.get('name')
                state = obj.get('state')
                district = obj.get('district')
                
                try:
                    if parent_subcategory and organization_name:
                        sub_category_object = TblSubcategories.objects.filter(id = parent_subcategory).first()
                        if sub_category_object:
                            organization_obj = TblOrganization.objects.filter(sub = parent_subcategory, org_name = organization_name).first()
                            
                            if organization_obj:
                                organization_obj.sub = sub_category_object
                                organization_obj.org_name = organization_name
                                organization_obj.state = state if state else organization_obj.state
                                organization_obj.district = district if district else organization_obj.district
                                organization_obj.save()
                                
                                response = {
                                        "id"                : organization_obj.id,
                                        "name"              : organization_obj.org_name,
                                        "state_id"          : organization_obj.state.id if organization_obj.state else '',
                                        "state"             : organization_obj.state.state_name if organization_obj.state else '',
                                        "district_id"       : organization_obj.district.id if organization_obj.district else '',
                                        "district"          : organization_obj.district.district_name if organization_obj.district else '',
                                        "category_id"       : organization_obj.sub.category.id if organization_obj.sub and organization_obj.sub.category else '',
                                        "category_name"     : organization_obj.sub.category.categories_name if organization_obj.sub and organization_obj.sub.category else '',
                                        "sub_category_id"   : organization_obj.sub.id if organization_obj.sub else '',
                                        "sub_category_name" : organization_obj.sub.subcategories_name if organization_obj.sub else ''
                                    }
                                
                                final_response.append(response)
                            
                            else:
                                organization_obj = TblOrganization(org_name = organization_name,
                                                                        state = state,
                                                                        district = district,
                                                                        sub = sub_category_object)
                            
                                organization_obj.save()
                                
                                response = {
                                    "id"                : organization_obj.id,
                                    "name"              : organization_obj.org_name,
                                    "state_id"          : organization_obj.state.id if organization_obj.state else '',
                                    "state"             : organization_obj.state.state_name if organization_obj.state else '',
                                    "district_id"       : organization_obj.district.id if organization_obj.district else '',
                                    "district"          : organization_obj.district.district_name if organization_obj.district else '',
                                    "category_id"       : organization_obj.sub.category.id if organization_obj.sub and organization_obj.sub.category else '',
                                    "category_name"     : organization_obj.sub.category.categories_name if organization_obj.sub and organization_obj.sub.category else '',
                                    "sub_category_id"   : organization_obj.sub.id if organization_obj.sub else '',
                                    "sub_category_name" : organization_obj.sub.subcategories_name if organization_obj.sub else ''
                                }
                                    
                                final_response.append(response)
                
                except Exception as e:
                    err_message = f"Error while adding organization :- {organization_name} as {str(e)}"
                    message.append(err_message)
                    
                if message:
                    return True, final_response, message
                
                else:
                    return True, final_response, "organization Added successfully"
            
        return False, {}, "organization is empty"
                    
    except Exception as e:
        print(f"Error in adding organization in database as {str(e)}")
        return False, {}, str(e)

def update_orgs(data):
    try:
        organization_id = data.get("id")
        
        if not organization_id:
            raise Exception("organization_id id is none")
        
        organization_obj = TblOrganization.objects.filter(id = organization_id).first()
        
        if not organization_obj:
            raise Exception("organization not found")
        
        for key, value in data.items():
            if key == "name":
                organization_obj.org_name = value
            if key == "state":
                organization_obj.state = value
            if key == 'district':
                organization_obj.district = value
            if key == 'sub_id':
                sub_category_object = TblSubcategories.objects.filter(id = value).first()
                if sub_category_object:
                    organization_obj.sub = sub_category_object
                
                
            organization_obj.save()
            
        organization_obj.save()
        
        response = {
                    "id"                : organization_obj.id,
                    "name"              : organization_obj.org_name,
                    "state_id"          : organization_obj.state.id if organization_obj.state else '',
                    "state"             : organization_obj.state.state_name if organization_obj.state else '',
                    "district_id"       : organization_obj.district.id if organization_obj.district else '',
                    "district"          : organization_obj.district.district_name if organization_obj.district else '',
                    "category_id"       : organization_obj.sub.category.id if organization_obj.sub and organization_obj.sub.category else '',
                    "category_name"     : organization_obj.sub.category.categories_name if organization_obj.sub and organization_obj.sub.category else '',
                    "sub_category_id"   : organization_obj.sub.id if organization_obj.sub else '',
                    "sub_category_name" : organization_obj.sub.subcategories_name if organization_obj.sub else ''
                }
        
        return True, response, "sub_category updated successfully"
        
    except Exception as e:
        print(f"Error in updating sub_category in database as {str(e)}")
        return False, {}, str(e)

def delete_orgs(data):
    try:
        org_id = data.get("id")
        
        if not org_id:
            raise Exception("organization id is none")
        
        organization_obj = TblOrganization.objects.filter(id=org_id).first()

        if not organization_obj:
            raise Exception("organization not found")
        
        TblProducts.objects.filter(organization=org_id).update(organization=None)

        # Delete subcategories and then the category
        organization_obj.delete()
                
        return True, {}, "organization deleted successfully"
        
    except Exception as e:
        print(f"Error in deleting organization from database as {str(e)}")
        return False, {}, str(e)




def get_products(data):
    try:
        final_response = []
        user_id = data.get('user_id')
        if not user_id:
            raise Exception("User is null")
        
        user_obj = TblUser.objects.filter(id = user_id).first()
        if not user_obj:
            raise Exception("User is not present")
        
        category = data.get("category")
        sub_category = data.get('sub_category')
        organization = data.get('organization')
        
        query = Q()
        
        if category:
            query &= Q(product_category=category)  # Using icontains for case-insensitive search

        if sub_category:
            query &= Q(product_sub_category=sub_category)

        if organization:
            query &= Q(organization=organization)
        
        if query:
            products_obj = TblProducts.objects.filter(query)
            
        else:
            products_obj = TblProducts.objects.all()
            
        products_images = {}
        for product_object in products_obj:
            images_list = ast.literal_eval(product_object.product_image)
            for i in range(len(images_list)):
                products_images[f"image_{i+1}"] = images_list[i]
            response = {
                        "id"                    : product_object.id,
                        "name"                  : product_object.product_name,
                        "organization_id"       : product_object.product_category_id if product_object.product_category else '',
                        "organization_name"     : product_object.product_category.categories_name if product_object.product_category else '',
                        "sub_category_id"       : product_object.product_sub_category_id if product_object.product_sub_category else '',
                        "sub_category_name"     : product_object.product_sub_category.subcategories_name if product_object.product_sub_category else '',
                        "product_organization_id"  : product_object.organization.id if product_object.organization else '',
                        "product_organization"  : product_object.organization.org_name if product_object.organization else '',
                        "price"                 : product_object.price,
                        "description"           : product_object.description,
                        "product_image"         : products_images,
                        "size_available"        : product_object.size_available
                        }
            
            final_response.append(response)
            
        return True, final_response, "Products fetched successully"
        
        
    except Exception as e:
        print(f"Error in fetching products from database as {str(e)}")
        return False, {}, str(e)

def add_products(user_id, data):
    try:
        final_response = []
        message = []
        
        for obj in data:
            serializer = add_products_serializer(data=obj)
            serializer.is_valid(raise_exception=True)
            
            product_name            = obj.get('name')
            product_category        = obj.get('category')
            product_sub_category    = obj.get('sub_category')
            product_organization    = obj.get('organization')
            price                   = obj.get('price')
            description             = obj.get('description')
            product_image           = obj.get('image')
            size                    = obj['size'] if 'size' in obj else {}
            state                   = obj.get('state')
            district                = obj.get('district')
            
            try:
                if product_category and product_sub_category:
                    category_object     = TblCategories.objects.filter(id=product_category).first()
                    if not category_object:
                        raise Exception(f"category not available as id {product_category}")
                    
                    sub_category_object = TblSubcategories.objects.filter(id=product_sub_category).first()
                    if not sub_category_object:
                        raise Exception(f"sub_category not available as id {product_sub_category}")
                
                
                if not product_category:
                    category_object = TblCategories.objects.filter(categories_name = "Global").first()
                    product_category = category_object.id
                    
                if not product_sub_category:
                    sub_category_object = TblSubcategories.objects.filter(subcategories_name = "Global").first()
                    product_sub_category = sub_category_object.id
                    
                if product_organization:
                    product_organization = TblOrganization.objects.filter(org_name = product_organization).first()
                    if not product_organization:
                        raise Exception(f"Organization not available as id {product_organization}")

                    state = product_organization.state if not state else state
                    
                    district = product_organization.district if not district else district
                
                query = Q()
                
                if product_category:
                    query &= Q(product_category=product_category)  # Using icontains for case-insensitive search

                if product_sub_category:
                    query &= Q(product_sub_category=product_sub_category)

                if product_organization:
                    query &= Q(organization=product_organization)
                    
                if state:
                    query &= Q(organization=state)
                    
                if district:
                    query &= Q(organization=district)
                
                
                product_object = TblProducts.objects.filter(query).first()

                product_images = []
                if product_object and product_object.product_image:
                    product_images.extend(ast.literal_eval(product_object.product_image))
                    product_images.append(product_image)
                    
                else:
                    product_images.append(product_image)
                
                if product_object:
                    # Update existing product
                    product_object.product_name         = product_name if product_name else product_object.product_name
                    product_object.product_category     = category_object
                    product_object.product_sub_category = sub_category_object
                    product_object.organization         = product_organization
                    product_object.price                = price if price else product_object.price
                    product_object.description          = description if description else product_object.description
                    product_object.product_image        = str(product_images)
                    product_object.size_available       = json.dumps(size) if size else product_object.size_available
                    product_object.updated_on           = datetime.datetime.now(datetime.timezone.utc)
                    product_object.updated_by           = user_id
                else:
                    # Create new product
                    product_object = TblProducts(
                        product_name=product_name,
                        product_category=category_object,
                        product_sub_category=sub_category_object,
                        price=price,
                        description=description,
                        product_image=str(product_images),
                        size_available=json.dumps(size),
                        created_on=datetime.datetime.now(datetime.timezone.utc).astimezone(gettz('Asia/Kolkata')),
                        created_by=user_id,
                        updated_on=datetime.datetime.now(datetime.timezone.utc).astimezone(gettz('Asia/Kolkata')),
                        updated_by=user_id,
                        state   = state,
                        district    = district,
                        organization    = product_organization
                    )
                
                product_object.save()
                
                products_images = {}
                images_list = ast.literal_eval(product_object.product_image)
                for i in range(len(images_list)):
                    products_images[f"image_{i+1}"] = images_list[i]
                size_dict = product_object.__dict__['size_available']
                response = {
                        "id"                    : product_object.id,
                        "name"                  : product_object.product_name,
                        "organization_id"       : product_object.product_category_id if product_object.product_category else '',
                        "organization_name"     : product_object.product_category.categories_name if product_object.product_category else '',
                        "sub_category_id"       : product_object.product_sub_category_id if product_object.product_sub_category else '',
                        "sub_category_name"     : product_object.product_sub_category.subcategories_name if product_object.product_sub_category else '',
                        "product_organization_id"  : product_object.organization.id if product_object.organization else '',
                        "product_organization"  : product_object.organization.org_name if product_object.organization else '',
                        "price"                 : product_object.price,
                        "description"           : product_object.description,
                        "product_image"         : products_images,
                        "size_available"        : json.loads(size_dict)
                        }
                
                final_response.append(response)
            
            except Exception as e:
                err_message = f"Error while adding product '{product_name}': {str(e)}"
                message.append(err_message)

        if message:
            return True, final_response, message
        else:
            return True, final_response, "Products added successfully"
        
    except Exception as e:
        print(f"Error in adding product to the database: {str(e)}")
        return False, {}, str(e)

      
def update_products(data):
    try:
        product_id = data.get("id")
        
        if not product_id:
            raise Exception("Product id is none")
        
        product_object = TblProducts.objects.filter(id=product_id).first()
        
        if not product_object:
            raise Exception("Product not found")
        
        for key, value in data.items():
            if key == "name":
                product_object.product_name = value
                
            elif key == "image":
                product_images = []
                if product_object and product_object.product_image:
                    product_images.extend(ast.literal_eval(product_object.product_image))
                    product_images.append(value)
                else:
                    product_images.append(value)
                product_object.product_image = str(product_images)
                
            elif key == "price":
                product_object.price = value
                
            elif key == "organization":
                org_object = TblOrganization.objects.filter(id=value).first()
                if not org_object:
                    raise Exception("Organization not found")
                product_object.organization = org_object
                
            elif key == "sub_category":
                sub_cat_object = TblSubcategories.objects.filter(id=value).first()
                if not sub_cat_object:
                    raise Exception("Sub-category not found")
                product_object.product_sub_category = sub_cat_object
                
            elif key == "category":
                cat_object = TblCategories.objects.filter(id=value).first()
                if not cat_object:
                    raise Exception("category not found")
                product_object.product_category = cat_object
                
            elif key == "state":
                state_object = TblState.objects.filter(id=value).first()
                if not state_object:
                    raise Exception("state_object not found")
                product_object.state = state_object
                
            elif key == "district":
                district_object = TblDistrict.objects.filter(id=value).first()
                if not district_object:
                    raise Exception("district_object not found")
                product_object.district = district_object
                
            elif key == "description":
                product_object.description = value
                
            elif key == "size":
                product_object.size_available = json.dumps(value)  # Ensure value is converted to a JSON string
            
        product_object.updated_by = data.get('user_id')
        product_object.size_available = json.dumps(product_object.size_available)
        product_object.save()
        
        products_images = {}
        images_list = ast.literal_eval(product_object.product_image)
        for i in range(len(images_list)):
            products_images[f"image_{i+1}"] = images_list[i]
        
        size_dict = product_object.__dict__['size_available']

        response = {
                    "id"                    : product_object.id,
                    "name"                  : product_object.product_name,
                    "organization_id"       : product_object.product_category_id if product_object.product_category else '',
                    "organization_name"     : product_object.product_category.categories_name if product_object.product_category else '',
                    "sub_category_id"       : product_object.product_sub_category_id if product_object.product_sub_category else '',
                    "sub_category_name"     : product_object.product_sub_category.subcategories_name if product_object.product_sub_category else '',
                    "product_organization_id"  : product_object.organization.id if product_object.organization else '',
                    "product_organization"  : product_object.organization.org_name if product_object.organization else '',
                    "price"                 : product_object.price,
                    "description"           : product_object.description,
                    "product_image"         : products_images,
                    "size_available"        : json.loads(size_dict)
                    }
        return True, response, "Product updated successfully"
        
    except Exception as e:
        print(f"Error in updating product in database: {str(e)}")
        return False, {}, str(e)


def delete_product(data):
    try:
        product_id = data.get("id")
        
        if not product_id:
            raise Exception("product_id  is none")
        
        product_obj = TblProducts.objects.filter(id = product_id).first()

        if not product_obj:
            raise Exception("product not found")
        
        product_obj.delete()
                
        return True, {}, "product deleted successfully"
        
    except Exception as e:
        print(f"Error in deleting product from database as {str(e)}")
        return False, {}, str(e)



    
    