from flask import request
from models import *
from errors import *
import time, os
from flask_jwt_extended import get_jwt_identity


def get_all_products_controller():
    """
    Get all products based on specified filters.

    This function retrieves a list of products based on optional query parameters.

    Query Parameters:
    - limit: Number of products per page (default is 5).
    - page: Page number for pagination (default is 1).
    - category: Filter by category name.
    - keyword: Search keyword.
    - max_price: Maximum price filter.
    - min_price: Minimum price filter.
    - order_by: Field to order by (e.g., 'price', 'name').
    - sort: Sorting order ('asc' for ascending, 'desc' for descending).

    Returns:
    - dict: A dictionary containing product data based on the specified filters.

    Raises:
    - DatabaseError: If the specified category is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Retrieve query parameters from the request
        limit = int(request.args.get("limit", 5))
        page = int(request.args.get("page", 1))
        category = request.args.get("category")
        keyword = request.args.get("keyword")
        max_price = request.args.get("max_price")
        min_price = request.args.get("min_price")
        order_by = request.args.get("order_by")
        sort = request.args.get("sort")
        
        # Check if the specified category exists in the database
        if not get_category_name(category):
            raise DatabaseError(f"The category '{category}' does not exist.")
        
        # Call the model function to fetch products based on the filters
        data = get_all_products(
            page=page,
            limit=limit,
            category=category,
            keyword=keyword,
            max_price=max_price,
            min_price=min_price,
            order_by=order_by,
            sort=sort
        )
        
        # Return the fetched data
        if data:
            return data
        else:
            return {"data": []}
    except DatabaseError as e:
        # Handle DatabaseError with appropriate error message
        return {"message": str(e), "data": []}, 404
    except Exception as e:
        # Handle other unexpected errors by raising them
        raise e


def get_products_by_category_controller(category_id: int):
    """
    Get products belonging to a specific category.

    This function retrieves products that belong to the specified category ID.

    Parameters:
    - category_id (int): The ID of the category.

    Returns:
    - dict: A dictionary containing category information along with its associated products.

    Raises:
    - DatabaseError: If the specified category ID is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Check if the specified category ID exists in the database
        if get_category(category_id) is None:
            raise DatabaseError(f"The category with ID {category_id} was not found.")
        
        # Retrieve products belonging to the specified category
        products = get_products_by_category(category_id)
        
        # Get category information
        category = get_category(category_id)
        
        # Add products to the category dictionary
        if products:
            category["products"] = products
        else:
            category["products"] = []
        
        # Return the category with its associated products
        return category
    except DatabaseError as e:
        # Handle DatabaseError with appropriate error message
        return {"message": str(e)}, 404
    except Exception as e:
        # Handle other unexpected errors by raising them
        raise e

def get_product_by_id_controller(id: int):
    """
    Controller function to retrieve a product based on a specified product ID.

    Parameters:
    - id (int): The ID of the product to be retrieved.

    Returns:
    - dict or tuple: A dictionary containing the product information or an error message with status code.
      If the product ID is not provided or is empty, the dictionary contains a "message" key with an error message and a 404 status code.
      If the product ID is not found, the dictionary contains a "message" key with an error message and a 404 status code.
      If the product is found, the dictionary contains the product information.
    """
    try:
        if not id or id == "":
            raise ValueError("ID produk harus diisi.")
        product = get_product_by_id(id)
        if product is None:
            raise DatabaseError(f"produk dengan ID {id} tidak ditemukan")
        return product
    except ValueError as e:
        return {"message": str(e)},422
    except DatabaseError as e:
        return {"message": str(e),"data":[]},404
    except Exception as e:
        raise e


def add_product_controller():
    """
    Add a new product to the database along with its images.

    This function handles the addition of a new product to the database. It also handles the upload of product images.

    Returns:
    - dict: A message indicating the success or failure of the product upload.

    Raises:
    - ValueError: If any required input fields are missing or if the file type is not allowed.
    - DatabaseError: If the specified category ID is not found in the database.
    - Exception: For other unexpected errors.
    """
    locations = []
    try:
        # Get current user identity from JWT token
        current_user = get_jwt_identity()
        # Check if the current user has admin role
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 403
        
        # Retrieve product information from request form data
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category_id = request.form.get("category_id")
        
        # Check if all required input fields are provided
        if not name or not description or not price or not quantity or not category_id:
            raise ValueError("All input fields are required.")
        
        # Check if the specified category ID exists in the database
        if not get_category(category_id):
            raise DatabaseError(f"The category with ID {category_id} was not found.")
        
        # Check if file is included in the request
        if "file" not in request.files:
            raise ValueError("Please include the image file.")
        
        # Retrieve and validate file(s) from the request
        files = request.files.getlist("file")
        if not files:
            raise ValueError("No selected files")
        allowed_files = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
        for file in files:
            if file.content_type not in allowed_files:
                raise ValueError("File type not allowed")
        
        # Upload image files and save their locations
        for file in files:
            location = "static/uploads/" + str(time.time()) + "_" + file.filename
            file.save(location)
            locations.append(location)
        
        # Upload product information to the database
        last_inserted_id = upload_product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
        )
        
        # Upload product images to the database
        upload_product_images(locations, last_inserted_id)
        
        # Return success message
        return {"message": "Product upload successful"}, 200
    
    except ValueError as ve:
        # Handle ValueError with appropriate error message
        return {"message": str(ve)}, 422
    
    except DatabaseError as e:
        # Handle DatabaseError with appropriate error message
        return {"message": str(e)}, 404
    
    except Exception as e:
        # If an unexpected error occurs, remove uploaded files and raise the error
        for file in locations:
            if os.path.exists(location):
                os.remove(location)
        raise e


def update_product_controller(product_id: int):
    """
    Update product information in the database.

    This function handles the update of product information in the database. It checks the user role,
    verifies if the product exists, validates input fields, and updates the product details.

    Args:
    - product_id (int): The ID of the product to be updated.

    Returns:
    - dict: A message indicating the success or failure of the product update.

    Raises:
    - ValueError: If any required input fields are missing.
    - DatabaseError: If the specified category ID is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Get current user identity from JWT token
        current_user = get_jwt_identity()
        # Check if the current user has admin role
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 401
        
        # Check if the product exists
        if get_product_by_id(product_id) is None:
            return {"message": f"Product with ID {product_id} not found"}, 404
        
        # Retrieve product information from request form data
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category_id = request.form.get("category_id")
        
        # Check if all required input fields are provided
        if not name or not description or not price or not quantity or not category_id:
            raise ValueError("All input fields are required.")
        
        # Check if the specified category ID exists in the database
        if get_products_by_category(category_id) is None:
            raise DatabaseError(f"Category with ID {category_id} not found.")
        
        # Update product information in the database
        update_product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
        )
        
        # Return success message
        return {"message": "Product update successful"}, 200
    
    except ValueError as ve:
        # Handle ValueError with appropriate error message
        return {"message": str(ve)}, 422
    
    except DatabaseError as e:
        # Handle DatabaseError with appropriate error message
        return {"message": str(e), "data": []}, 422
    
    except Exception as e:
        # If an unexpected error occurs, raise the error
        return e
    


def delete_product_controller(product_id: int):
    """
    Delete a product from the database.

    This function handles the deletion of a product from the database. It checks the user role,
    verifies if the product exists, deletes the product and associated images, and returns a success message.

    Args:
    - product_id (int): The ID of the product to be deleted.

    Returns:
    - dict: A message indicating the success or failure of the product deletion.

    Raises:
    - Unauthorized: If the user is not authorized to delete products.
    - DatabaseError: If the specified product ID is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Get current user identity from JWT token
        current_user = get_jwt_identity()
        # Check if the current user has admin role
        if current_user["role"] != "admin":
            raise Unauthorized("Unauthorized")
        
        # Check if the product exists
        if get_product_by_id(product_id):
            # Retrieve all images associated with the product
            images = get_all_product_images(product_id=product_id)
            # Delete the product from the database
            delete_product(product_id)
            # Delete associated images from the server
            for image in images:
                if os.path.exists(image["image"]):
                    os.remove(image["image"])
            return {"message": "Product deletion successful"}
        # If product not found, raise DatabaseError
        raise DatabaseError("Product ID not found")
    
    except Unauthorized as e:
        # Handle Unauthorized exception with appropriate error message
        return {"message": str(e)}, 403
    
    except DatabaseError as ve:
        # Handle DatabaseError with appropriate error message
        return {"message": str(ve)}, 404
    
    except Exception as e:
        # If an unexpected error occurs, raise the error
        raise e

# PRODUCT IMAGES MODELS


def all_product_images_controller(product_id: int):
    """
    Retrieve all images associated with a product.

    This function retrieves all images associated with a specified product from the database,
    combines them with the product information, and returns the result.

    Args:
    - product_id (int): The ID of the product to retrieve images for.

    Returns:
    - dict: A dictionary containing product information along with a list of associated images.

    Raises:
    - DatabaseError: If the specified product ID is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Check if the product exists
        if get_product_by_id(product_id) is None:
            raise DatabaseError(f"Product with ID {product_id} not found")
        
        # Retrieve all images associated with the product and the products
        images = get_all_product_images(product_id)
        product = get_product_by_id(product_id)
        # Combine product information with images and return
        product["images"] = images
        return product
    
    except DatabaseError as ve:
        # Handle DatabaseError with appropriate error message
        return {"message": str(ve), "data": []}, 404
    
    except Exception as e:
        # If an unexpected error occurs, raise the error
        raise e
    
def upload_image_controller(product_id: int):
    """
    Upload images for a specific product.

    This function handles the uploading of images for a specified product.
    It checks if the user is authorized to perform this action, validates the uploaded files,
    saves them to the server, associates them with the specified product, and returns a success message.

    Args:
    - product_id (int): The ID of the product to upload images for.

    Returns:
    - dict: A dictionary containing a success message indicating that the product images were successfully uploaded.

    Raises:
    - ValueError: If the request does not contain a file or if the file type is not allowed, or if the product ID is missing.
    - Unauthorized: If the user is not authorized to perform this action.
    - Exception: For other unexpected errors.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            raise Unauthorized("Unauthorized")
        
        # Check if files are present in the request
        if "file" not in request.files:
            raise ValueError("No file part")
        
        files = request.files.getlist("file")
        if not files:
            raise ValueError("No selected files")
        
        allowed_files = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
        for file in files:
            # Validate file types
            if file.content_type not in allowed_files:
                raise ValueError("File type not allowed")
        
        locations = []
        for file in files:
            # Save files to the server
            location = "static/uploads/" + str(time.time()) + "_" + file.filename
            file.save(location)
            locations.append(location)
        
        if not product_id or product_id == "":
            raise ValueError("Please provide a product ID")
        
        # Check if the product exists
        if get_product_by_id(product_id) is None:
            return {"message": f"Product with ID {product_id} not found"}, 404
        
        # Associate uploaded images with the product
        upload_product_images(image_location=locations, product_id=product_id)
        return {"message": "Product images uploaded successfully"}, 200
    
    except ValueError as ve:
        return {"message": str(ve)}, 422
    except Unauthorized as e:
        return {"message": str(e)}, 403
    except Exception as e:
        # If an unexpected error occurs, remove uploaded files and raise the error
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e

    
def get_image_by_id_controller(product_id: int, image_id: int):
    """
    Retrieve an image by its ID for a specific product.

    This function retrieves an image by its ID for a specified product.
    It checks if both the product and the image exist in the database, and returns the image data if found.

    Args:
    - product_id (int): The ID of the product to which the image belongs.
    - image_id (int): The ID of the image to retrieve.

    Returns:
    - dict: A dictionary containing the image data if found.

    Raises:
    - Unauthorized: If the user is not authorized to access this resource.
    - DatabaseError: If the specified product or image is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Check if the product exists
        if get_product_by_id(product_id) is None:
            raise DatabaseError(f"Product with ID {product_id} not found")
        
        # Check if the image exists for the specified product
        image = get_image_by_product_id_and_image_id(product_id, image_id)
        if image is None:
            raise DatabaseError(f"Image with ID {image_id} not found")  
        return image
    
    except Unauthorized as e:
        return {"message": str(e)}, 422
    except DatabaseError as e:
        return {"message": str(e), "data": []}, 404
    except Exception as e:
        raise e
    

def delete_image_by_id_controller(product_id: int, image_id: int):
    """
    Delete an image by its ID for a specific product.

    This function deletes an image by its ID for a specified product.
    It checks if the user is authorized to perform this action, and if both the product and the image exist in the database.

    Args:
    - product_id (int): The ID of the product to which the image belongs.
    - image_id (int): The ID of the image to delete.

    Returns:
    - dict: A dictionary containing a success message if the deletion is successful.

    Raises:
    - DatabaseError: If the specified product or image is not found in the database.
    - Unauthorized: If the user is not authorized to perform this action.
    - Exception: For other unexpected errors.
    """
    try:
        # Check if the user is authorized
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            raise Unauthorized("Unauthorized")
        
        # Check if the product exists
        if get_product_by_id(product_id) is None:
            raise DatabaseError(f"Product with ID {product_id} not found")
        
        # Check if the image exists for the specified product
        image = get_image_by_product_id_and_image_id(product_id, image_id)
        if image is None:
            raise DatabaseError(f"Image with ID {image_id} not found")
        
        # Delete the image file from the filesystem
        if os.path.exists(image["image"]):
            os.remove(image["image"])
        
        # Delete the image from the database
        delete_image_by_id(image_id, product_id)
        return {"message": "Image successfully deleted"}, 200
    
    except DatabaseError as e:
        return {"message": str(e)}, 404
    except Unauthorized as e:
        return {"message": str(e)}, 422
    except Exception as e:
        raise e

def delete_images_by_product_id_controller(product_id: int):
    """
    Delete all images associated with a product.

    This function deletes all images associated with a specified product ID.
    It checks if the user is authorized to perform this action and if the product exists in the database.

    Args:
    - product_id (int): The ID of the product whose images are to be deleted.

    Returns:
    - dict: A dictionary containing a success message if the deletion is successful.

    Raises:
    - Unauthorized: If the user is not authorized to perform this action.
    - DatabaseError: If the specified product is not found in the database.
    - Exception: For other unexpected errors.
    """
    try:
        # Get the current user identity
        current_user = get_jwt_identity()
        
        # Check if the user is authorized to delete images
        if current_user["role"] != "admin":
            raise Unauthorized("Unauthorized")
        
        # Check if the product exists
        if get_all_product_images(product_id) is None:
            raise DatabaseError(f"Product with ID {product_id} not found")
        
        # Get all images associated with the product
        images = get_all_product_images(product_id=product_id)
        
        # Delete all images from the database and filesystem
        delete_images_by_product_id(product_id)
        for image in images:
            if os.path.exists(image["image"]):
                os.remove(image["image"])
        return {"message": "All images successfully deleted"}, 200
    
    except Unauthorized as e:
        return {"message": str(e)}, 403
    except DatabaseError as e:
        return {"message": str(e)}, 404
    except Exception as e:
        raise e
