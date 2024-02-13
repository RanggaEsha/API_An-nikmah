from flask import request 
from models import *
from flask_jwt_extended import (get_jwt_identity)
from errors import *
from form_validator import add_category_form

def get_categories_controller():
    """
    Controller function to retrieve all categories.

    Returns:
    - list: A list containing dictionaries with category information including category ID and name.
    """
    return get_categories()

def get_category_controller(id: int):
    """
    Retrieves category information based on ID.

    Parameters:
        id (int): The ID of the category to retrieve.

    Returns:
        dict: Information about the category if found.
        dict: Error message if the category is not found.
    """
    try:
        # Checking if the category with the given ID is found
        if get_category(id) is None:
            raise ValueError(f'Category with ID {id} not found')
        return get_category(id)
    except ValueError as e:
        # Returning an error message if the category is not found
        return {"error": str(e)}, 422
    except Exception as e:
        # Returning an error if any other error occurs
        raise e

def add_category_controller():
    """
    Controller function to add a new category.

    Returns:
    - dict: A dictionary containing a success message if the category is added successfully, or an error message with a 404 status code if the category name is already registered.
    """
    try:
        # Checking user role
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            raise Unauthorized('Unauthorized')
        
        # Retrieving category name from the request
        name = request.form.get('name')
        form = add_category_form(request.form)
        
        # validating value of name in form
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Checking if the category name is already registered
        if get_category_name(name):
            raise DatabaseError('Category name is already registered')
        
        # Adding the category
        add_category(name)
        
        # Returning success message
        return {'message': 'Category added successfully'}, 200
    
    except ValueError as e:
        # Returning an error message if adding category value is wrong
        return {"errors": e.args[0]}, 422
    except DatabaseError as e:
        # Returning error message if there's a database error
        return {"error": str(e)}, 404
    except Unauthorized as e:
        # Returning unauthorized message
        return {"error": str(e)}, 422
    except Exception as e:
        # Raising other exceptions
        raise e


def update_category_controller(id: int):
    """
    Controller function to update an existing category.

    Parameters:
        id (int): The ID of the category to update.

    Returns:
    - dict: A dictionary containing a success message if the category is updated successfully, or an error message with a 404 status code if the category ID is not found, or an error message with a 422 status code if the user is not authorized or if the category name is already registered.
    """
    try:
        # Checking user role
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            raise Unauthorized('Unauthorized')
        
        # Retrieving category name from the request
        name = request.form.get('name')

        # checking wheither form name is fulfilled correctly
        form = add_category_form(request.form)
        
        # validating value of name in form
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Checking if the category with the given ID exists
        if get_category(id) is None:
            raise DatabaseError(f'Category with ID {id} not found')
        
        # Checking if the category name is already registered
        if get_category_name(name):
            raise DatabaseError('Category name is already registered')
        
        # Updating the category
        update_category(id, name)
        return {'message': 'Category updated successfully'}, 200
    except ValueError as e:
        return {"errors": e.args[0]}, 404
    except DatabaseError as e:
        return {"error": str(e)}, 404
    except Unauthorized as e:
        return {"error": str(e)}, 422
    except Exception as e:
        raise e

def delete_category_controller(id):
    """
    Controller function to delete a category.

    Parameters:
        id (int): The ID of the category to delete.

    Returns:
    - dict: A dictionary containing a success message if the category is deleted successfully, or an error message with a 404 status code if the category ID is not found, or an error message with a 422 status code if the user is not authorized.
    """
    try:
        # Checking user role
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            raise Unauthorized('Unauthorized')
        
        # Checking if the category with the given ID exists
        if get_category(id):
            # Deleting the category
            delete_category(id)
            return {'message': 'Category deleted successfully'}, 200
        
        # Raising error if category ID is not found
        raise DatabaseError(f"Category with ID {id} not found")
    
    except Unauthorized as e:
        return {"error": str(e)}, 422
    except DatabaseError as e:
        return {"error": str(e)}, 404
    except Exception as e:
        raise e
