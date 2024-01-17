from flask import request
from flask_jwt_extended import (create_access_token,get_jwt_identity)
from models import *

def protected_controller():
    current_user = get_jwt_identity()
    return {'login as':current_user},200


def login_controller():
    email = request.form.get('email')
    password = request.form.get('password')
    user = find_email_password(email=email, password=password)

    if user:
        access_token = create_access_token(identity=user["username"])
        return {'token': access_token}
    return {"msg": "Username atau password salah"}, 401


def register_controller():
    register_user = find_email(request)
    if register_user:
       return {'message': 'email sudah terdaftar'}, 404
    
    add_user_data(request)
    return {'message': 'register berhasil'}, 200