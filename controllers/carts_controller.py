from models import *
from errors import *
from flask import request
from flask_jwt_extended import get_jwt_identity
from form_validator import get_cart_form,add_cart_form,validate_date_format

def get_carts_user_controller():
    """
    Controller function to retrieve carts belonging to the current user.

    Returns:
        dict: A dictionary containing cart data if found.
        dict: Error message with status code 404 if carts are not found.
        dict: Error message with status code 422 for other exceptions.
    """
    try:
        # Retrieving query parameters
        limit = request.args.get('limit', 5)
        page = request.args.get('page', 1)
        max_date = request.args.get('max_date')
        min_date = request.args.get('min_date')
        # Check if either max_date or min_date is provided in the request
        if max_date or min_date:

            # Validate format of max_date if it's present
            if max_date and not validate_date_format(max_date):
                # Raise an error with a message about invalid max_date format
                errors = {"max_date": ["Invalid date format. Use YYYY-MM-DD."]}
                raise ValueError(errors)

            # Validate format of min_date if it's present
            if min_date and not validate_date_format(min_date):
                # Raise an error with a message about invalid min_date format
                errors = {"min_date": ["Invalid date format. Use YYYY-MM-DD."]}
                raise ValueError(errors)

            # Create a form instance from request.form data
            form = get_cart_form(request.form)

            # Perform additional validation on the form
            if not form.validate():
                # Collect errors from the form fields
                errors = {field.name: field.errors for field in form if field.errors}
                # Raise a ValueError with the collected form errors
                raise ValueError(errors)

        
        # Checking if the user is an admin
        if get_jwt_identity()['role'] == 'admin':
            # If admin, retrieve all carts
            return get_all_carts(page, limit, max_date, min_date)
        
        # If not admin, retrieve carts for the current user
        user_id = get_jwt_identity()["id"]
        user_carts = get_carts_by_user_id(user_id, page, limit, max_date, min_date)
        
        # If user carts are empty, raise an error
        if not user_carts:
            raise DatabaseError("Your shopping cart is empty")
        return user_carts
    except ValueError as e:
        return {"errors": e.args[0]}, 422
    except DatabaseError as e:
        return {"error": str(e), "data": []}, 404
    except Exception as e:
        raise e

    
def add_carts_user_controller():
    """
    Controller function to add a product to the user's cart or update the quantity if the product is already in the cart.

    Returns:
        dict: A dictionary containing a success message if the operation is successful.
        dict: Error message if the operation fails.
    """
    try:
        # Getting the user ID from the JWT token
        user_id = get_jwt_identity()["id"]
        
        # Retrieving product ID and quantity from the request form
        product_id = request.form.get("product_id")
        quantity = request.form.get("quantity")
        form = add_cart_form(request.form)
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Retrieving product information
        product = get_product_by_id(product_id)
        
        # Checking if the product exists
        if product is None:
            raise DatabaseError(f"Product with ID {product_id} not found")
        
        # Checking if the requested quantity exceeds available stock
        if product['quantity'] < int(quantity):
            raise DatabaseError(f"Stock of product with ID {product_id} is only {product['quantity']} items")
        
        # Checking if the user already has the product in their cart
        if get_carts_by_user_id_and_product_id(user_id, product_id) is None:
            # If not, add the product to the cart
            add_carts(user_id, product_id, quantity)
            result = {"message": "Successfully added to cart"}, 200
            return result
        else:
            update_cart(product_id, user_id, quantity)
            # If yes, update the quantity in the cart
            result = {"message": "Quantity updated successfully"}, 200
            return result
    except ValueError as ve:
        return {"errors": ve.args[0]}, 422
    except DatabaseError as e:
        return {"error": str(e), "data": []}, 404
    except Exception as e:
        raise e


def delete_cart_by_user_id_controller():
    """
    Controller function to delete all carts belonging to the current user.

    Returns:
        dict: A dictionary containing a success message if the carts are deleted successfully.
        dict: Error message with status code 422 for ValueError exceptions.
        dict: Error message with status code 422 for other exceptions.
    """
    try:
        # Getting the user ID from the JWT token
        user_id = get_jwt_identity()["id"]
        
        # Deleting all carts associated with the user ID
        delete_cart_by_user_id(user_id)
        
        # Returning success message
        return {"message": "Successfully deleted all your carts"}
    except Exception as e:
        # Handling other exceptions and raising them
        raise e

def delete_cart_by_cart_id_and_user_id_controller(cart_id):
    """
    Controller function to delete a cart by its ID and the user's ID.

    Parameters:
        cart_id (int): The ID of the cart to be deleted.

    Returns:
        dict: A dictionary containing a success message if the cart is deleted.
        dict: Error message with status code 404 if the cart ID is not found in the database.
        dict: Error message with status code 422 for ValueError exceptions.
    """
    try:
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()["id"]
        
        # Check if the cart with the given cart_id and user_id exists
        if get_cart_by_cart_id_and_user_id(cart_id, user_id) is None:
            raise DatabaseError("cart ID is not found")
        
        # Delete the cart
        delete_cart_by_user_id_and_cart_id(cart_id, user_id)
        return {"message": "Successfully deleted your cart"}
    
    except DatabaseError as e:
        # Return error message for database errors
        return {"error": str(e)},404
    except Exception as e:
        # Raise any other exceptions
        raise e

