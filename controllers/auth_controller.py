from flask import request
from flask_jwt_extended import (create_access_token,get_jwt_identity)
from models import *
from datetime import timedelta

def protected_controller():
    current_user = get_jwt_identity()
    return {'login as':current_user["username"]},200


# USER

def get_email_password_controller():
    """
    Controller function to authenticate and generate an access token for the user.

    Returns:
    - dict: A dictionary containing an access token if authentication is successful, or an error message with a 401 status code if authentication fails.
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = find_email_password(email=email, password=password)
        if user:
            access_token = create_access_token(identity={"id":user[0]['id'],"username":user[1]["username"],"role":user[2]["role"]},expires_delta=timedelta(hours=1))
            return {'token': access_token}
        return {"msg": "Username atau password salah"}, 404
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422


def register_controller():
    """
    Controller function to register a new user.

    Returns:
    - dict: A dictionary containing a success message if registration is successful, or an error message with a 404 status code if the email is already registered.
    """
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        register_user = find_email(request)
        if register_user:
            raise ValueError('email sudah terdaftar')
        add_user_data(first_name,last_name,email,password)
        return {'message': 'register berhasil'}, 200
    except ValueError as ve:
        return {"message": str(ve)},404
    except Exception as e:
        return {"message": str(e)},422
    
def get_user_data_controller():
    try:
        user_id = get_jwt_identity()["id"]
        get_user_data(user_id)
    except Exception as e:
        return {"message": str(e)},422

def update_data_user_controller():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        update_data_user(first_name,last_name,email,password)
        return {'message': 'register berhasil'}, 200
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422
    
def delete_user_controller():
    try:
        user_id = get_jwt_identity()['id']
        delete_user(user_id)
        return {"message": "berhasil menghapus data user"}
    except Exception as e:
        return {"message": str(e)},422

# ADMIN 

    
def register_admin_controller():
    """
    Controller function to register a new user.

    Returns:
    - dict: A dictionary containing a success message if registration is successful, or an error message with a 404 status code if the email is already registered.
    """
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        register_user = find_email(request)
        if register_user:
            raise ValueError('email sudah terdaftar')
        add_admin_data(first_name,last_name,email,password)
        return {'message': 'register berhasil'}, 200
    except ValueError as ve:
        return {"message": str(ve)},404
    except Exception as e:
        return {"message": str(e)},422
    
def get_admin_data_controller():
    try:
        admin = get_jwt_identity()
        print(admin)
        admin_id = admin["id"]
        if admin['role'] != 'admin':
            raise Exception("Unauthorized")
        return get_user_data(admin_id)
    except Exception as e:
        return {"message": str(e)},422

def update_data_admin_controller():
    try:
        admin = get_jwt_identity()
        admin_id = admin["id"]
        if admin['role'] != 'admin':
            raise Exception("Unauthorized")
        data = get_user_data(admin_id)
        
        first_name = request.form.get('first_name',data["first_name"])
        last_name = request.form.get('last_name',data["last_name"])
        password = request.form.get('password',data["password"])
        email = request.form.get('email')
        if email:
            if find_email(request):
                raise ValueError('email sudah terdaftar')
        else:
            email = data['email']
        
        update_data_user(admin_id,first_name,last_name,email,password)
        return {'message': 'register berhasil'}, 200
    except ValueError as ve:
        return {"message": str(ve)},404
    except Exception as e:
        return {"message": str(e)},422
    
def delete_admin_controller():
    try:
        user_id=get_jwt_identity()['id']
        delete_user(user_id)
        return {"message": "berhasil menghapus data admin"}
    except Exception as e:
        return {"message": str(e)},422