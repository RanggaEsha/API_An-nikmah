from flask import request
from flask_jwt_extended import (create_access_token,get_jwt_identity)
from models import *
from datetime import timedelta
from errors import Unauthorized,DatabaseError
from form_validator import RegistrationForm,LoginForm



def protected_controller():
    current_user = get_jwt_identity()
    return {'login as':current_user["username"]},200

# USER

def get_email_password_controller():
    """
    Controller function to authenticate users based on email and password.

    Returns:
        dict: A dictionary containing an access token if authentication is successful.
        dict: Error message with a 422 status code if authentication fails.
    """
    try:
        # Retrieving email and password from the request form
        email = request.form.get('email')
        password = request.form.get('password')
        form = LoginForm(request.form)
        
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        # Finding user information based on email and password
        user = find_email_password(email=email, password=password)   
        
        # If user information is found, create an access token
        if user:
            access_token = create_access_token(
                identity={
                    "id": user['id'],
                    "username": user["username"],
                    "role": user["role"]
                },
                expires_delta=timedelta(hours=1)
            )
            return {'token': access_token}
        
        # If user information is not found, raise an error
        raise ValueError("Email atau password salah")
    
    except ValueError as e:
        # Returning an error message if authentication fails
        return {"errors": e.args[0]}, 422
    
    except Exception as e:
        # Raising an error if any other error occurs
        raise e



def register_controller():
    """
    Controller function to register a new user.

    Returns:
        dict: A dictionary containing a success message if registration is successful.
        dict: Error message with a 404 status code if the email is already registered.
    """
    try:
        # Retrieving user information from the request form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        form = RegistrationForm(request.form)
        
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)

        register_user = find_email(request)
        if register_user:
            raise DatabaseError('Email sudah terdaftar')
        
        # Adding user data to the database
        add_user_data(first_name, last_name, email, password)
        return {'message': 'Register berhasil'}, 200
    
    except DatabaseError as e:
        return {"error": str(e)}, 404
    except ValueError as e:
        # Returning an error message if the email is already registered
        return {"errors": e.args[0]}, 422
    
    except Exception as e:
        # Raising an error if any other error occurs
        raise e

    
def get_user_data_controller():
    """
    Controller function to retrieve user data.

    Returns:
        dict: User data if retrieval is successful.
    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    try:
        # Getting the user ID from the JWT token
        user_id = get_jwt_identity()["id"]
        
        # Retrieving user data based on the user ID
        return get_user_data(user_id)
    
    except Exception as e:
        # Raising an error if any exception occurs during the process
        raise e


def update_data_user_controller():
    """
    Controller function to update user data.

    Returns:
        dict: Success message if the update is successful.
    Raises:
        ValueError: If there is a validation error.
        Exception: If an error occurs during the update process.
    """
    try:
        # Getting the user ID from the JWT token
        user = get_jwt_identity()
        user_id = user['id']
        if user['role'] != 'user':
            raise Unauthorized("Unauthorized")
        # Retrieving updated user data from the request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        form = RegistrationForm(request.form)
        
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Updating user data in the database
        update_data_user(user_id, first_name, last_name, email, password)
        return {'message': 'Data user berhasil diperbarui'}, 200
    except Unauthorized as e:
        # Handling unauthorized access
        return {"error": str(e)}, 422
    
    except ValueError as e:
        # Handling validation errors
        return {"errors": e.args[0]}, 422
    
    except Exception as e:
        # Raising an error if any exception occurs during the process
        raise e

    
def delete_user_controller():
    try:
        user_id = get_jwt_identity()['id']
        delete_user(user_id)
        return {"message": "berhasil menghapus data user"}
    except Exception as e:
        raise e

# ADMIN 

    
def register_admin_controller():
    """
    Controller function to register a new admin.

    Returns:
        dict: Success message if the registration is successful.
    Raises:
        ValueError: If there is a validation error.
        Exception: If an error occurs during the registration process.
    """
    try:
        # Retrieving user data from the request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        form = RegistrationForm(request.form)
        
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Checking if the email is already registered
        register_user = find_email(request)
        if register_user:
            raise ValueError('Email already registered')
        
        # Adding admin data to the database
        add_admin_data(first_name, last_name, email, password)
        
        return {'message': 'Registration successful'}, 200
    
    except ValueError as e:
        # Handling validation errors
        return {"errors": e.args[0] }, 404
    
    except Exception as e:
        # Raising an error if any exception occurs during the process
        raise e

    
def get_admin_data_controller():
    """
    Controller function to retrieve admin data.

    Returns:
        dict: Admin data if the request is authorized.
    Raises:
        Unauthorized: If the request is not authorized.
        Exception: If any other error occurs during the process.
    """
    try:
        # Getting the admin identity from the JWT token
        admin = get_jwt_identity()
        admin_id = admin["id"]
        
        # Checking if the user is an admin
        if admin['role'] != 'admin':
            raise Unauthorized("Unauthorized")
        
        # Retrieving admin data from the database and return it
        return get_user_data(admin_id)
    
    except Unauthorized as e:
        # Handling unauthorized access
        return {"error": str(e)}, 422
    except Exception as e:
        # Raising an error if any other exception occurs
        raise e


def update_data_admin_controller():
    """
    Controller function to update admin data.

    Returns:
        dict: Success message if the data is updated successfully.
    Raises:
        Unauthorized: If the request is not authorized.
        Exception: If any other error occurs during the process.
    """
    try:
        # Getting the admin identity from the JWT token
        admin = get_jwt_identity()
        admin_id = admin["id"]
        
        # Checking if the user is an admin
        if admin['role'] != 'admin':
            raise Unauthorized("Unauthorized")   
        
        # Getting data from the request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        email = request.form.get('email')
        form = RegistrationForm(request.form)
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Updating admin data in the database
        update_data_user(admin_id, first_name, last_name, email, password)
        return {'message': 'Data updated successfully'}, 200
    except ValueError as e:
        # Returning an error message if authentication fails
        return {"error": e.args[0]}, 422
    except Unauthorized as e:
        # Handling unauthorized access
        return {"error": str(e)}, 404
    except Exception as e:
        # Raising an error if any other exception occurs
        raise e

    
def delete_admin_controller():
    """
    Controller function to delete admin data.

    Returns:
        dict: Success message if the data is deleted successfully.
    Raises:
        Unauthorized: If the request is not authorized.
        Exception: If any other error occurs during the process.
    """
    try:
        # Getting the user ID from the JWT token
        user_id = get_jwt_identity()['id']
        
        # Checking if the user is an admin
        if get_jwt_identity()['role'] == "admin":
            # Deleting the user
            delete_user(user_id)
            return {"message": "Admin data deleted successfully"}
        else:
            # If the user is not an admin, raise unauthorized access
            raise Unauthorized("Unauthorized")
    
    except Unauthorized as e:
        # Handling unauthorized access
        return {"error": str(e)}, 422
    except Exception as e:
        # Raising an error if any other exception occurs
        raise e
