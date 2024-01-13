from flask import request
from flask_jwt_extended import (create_access_token,get_jwt_identity)
from models import validator_register,register_proccess,login_process

def protected_controller():
    current_user = get_jwt_identity()
    return {'login as':current_user},200

from models import login_process

def login_controller():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login_process(email=email, password=password)

    if user:
        access_token = create_access_token(identity=user["username"])
        return {'token': access_token}
    
    return {"msg": "Username atau password salah"}, 401


def register_controller():
    register_user = validator_register(request)
    if register_user:
       return {'message': 'email sudah terdaftar'}, 404
    
    register_proccess(request)
    return {'message': 'register berhasil'}, 200