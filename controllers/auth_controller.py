from flask import request
from flask_jwt_extended import (create_access_token,get_jwt_identity)
from models import *
from datetime import timedelta

def protected_controller():
    current_user = get_jwt_identity()
    return {'login as':current_user["username"]},200


def get_email_password_controller():
    email = request.form.get('email')
    password = request.form.get('password')
    user = find_email_password(email=email, password=password)
    print(user)
    if user:
        access_token = create_access_token(identity={"id":user[0]['id'],"username":user[1]["username"],"role":user[2]["role"]},expires_delta=timedelta(hours=1))
        
        return {'token': access_token}
    return {"msg": "Username atau password salah"}, 401


def register_controller():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role',"user")
    register_user = find_email(request)
    if register_user:
       return {'message': 'email sudah terdaftar'}, 404
    add_user_data(first_name,last_name,email,password,role)
    return {'message': 'register berhasil'}, 200