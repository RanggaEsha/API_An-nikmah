from flask import Flask
from controllers import *



from flask_jwt_extended import (
    JWTManager,
    jwt_required,
)
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "bacotttttttt"
jwt = JWTManager(app)

@app.get('/protected')
@jwt_required()
def get_all_products():
    return protected_controller()

@app.post('/login')
def login_process():
    return login_controller()

@app.post('/register')
def register():
    return register_controller()

@app.get('/products')
def get_products():
    return get_all_products_controller()

@app.get('/products/<int:category_id>')
def products_by_category(category_id):
    return get_products_by_category_controller(category_id) 

@app.post('/products')
def upload():
    return add_product_controller()

@app.put('/products/<int:id>')
def update(id):
    return update_product_controller(id)

@app.delete('/products/<int:id>')
def delete(id):
    return delete_product_controller(id)

@app.get('/products/images/<int:product_id>')
def product_images(product_id):
    return all_product_images(product_id)

@app.post('/products/images')
def upload_image():
    return upload_image_controller()

@app.put('/products/images/<int:id>')
def update_image(id):
    return update_image_controller(id)

if __name__==('__main__'):
   app.run(debug=True,port=5001,use_reloader=True,host="0.0.0.0")