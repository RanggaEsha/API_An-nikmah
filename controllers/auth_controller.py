from auth.login import login
from flask import request
from flask_jwt_extended import create_access_token
from auth import validator_register,register_proccess


def login_controller():
   email = request.form.get('email')
   password = request.form.get('password')
   login_user = login(email=email,password=password)
   if login_user:
       access_token = create_access_token(identity=email)
       return {'token' : access_token}
   return {"msg": "Username atau password salah"}, 401

def register_controller():
    register_user = validator_register(request)
    if register_user:
       return {'message': 'email sudah terdaftar'}, 404
    
    register_proccess(request)
    return {'message': 'register berhasil'}, 200