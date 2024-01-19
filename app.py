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

# LOGIN AND REGISTER

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

# PRODUCTS

@app.get('/products')
def get_products():
    return get_all_products_controller()

@app.get('/products/<int:id>')
def products_by_id(id):
    return get_products_by_id_controller(id) 

@app.post('/products')
def upload():
    return add_product_controller()

@app.put('/products/<int:id>')
def update(id):
    return update_product_controller(id)


@app.delete('/products/<int:id>')
def delete(id):
    return delete_product_controller(id)

# IMAGES

@app.get('/products/<int:product_id>/images')
def product_images(product_id):
    return all_product_images(product_id)

@app.post('/products/images')
def upload_image():
    return upload_image_controller()

@app.delete('/products/<int:product_id>/images/<int:id>')
def delete_image(product_id,id):
   return delete_image_by_id_controller(product_id,id)

@app.delete('/products/<int:product_id>/images')
def delete_images(product_id):
    return delete_images_by_product_id_controller(product_id)

# CATEGORIES

@app.get('/categories')
def get_all_categories():
    return get_categories_controller()

@app.get('/category/<int:category_id>/products')
def products_by_category(category_id):
    return get_products_by_category_controller(category_id) 

@app.get('/categories/<int:id>')
def get_category_by_id(id):
    return get_category_controller(id)

@app.post('/categories')
def add_category():
    return add_category_controller()

@app.put('/categories/<int:id>')
def update_category_by_id(id):
    return update_category_controller(id)

@app.delete('/categories/<int:id>')
def delete_category_by_id(id):
    return delete_category_controller(id)

# CARTS
@app.get('/carts/<int:user_id>')
def get_user_carts(user_id):
    return get_carts_user_controller(user_id)

@app.post('/carts')
def add_user_carts():
    return add_carts_user_controller()



if __name__==('__main__'):
   app.run(debug=True,port=5001,use_reloader=True,host="0.0.0.0")