from flask import Flask, request
from auth.login import login
from auth.register import register1,validator_register
from models.product import upload_product
# from upload.image import upload_image
from db import conn
from controllers import product_controller


from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "bacotttttttt"
jwt = JWTManager(app)

@app.get('/products')
@jwt_required()
def get_all_products():
    current_user = get_jwt_identity()
    return {'login as':current_user},200
   

@app.post('/login')
def login_process():
   email = request.form.get('email')
   password = request.form.get('password')
   login_user = login(email=email,password=password)
   if login_user:
       access_token = create_access_token(identity=email)
       return {'token' : access_token}
   return {"msg": "Username atau password salah"}, 401


@app.post('/register')
def register():
    register_user = validator_register(request)
    if register_user:
       return {'message': 'email sudah terdaftar'}, 404
    
    register1(request)
    return {'message': 'register berhasil'}, 200
   
   
   
@app.post('/products')
def upload():
    return product_controller.add_product()

if __name__==('__main__'):
   app.run(debug=True,port=5001,use_reloader=True,host="0.0.0.0")