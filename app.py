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
def get_email_password():
    return get_email_password_controller()

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
@jwt_required()
def upload():
    return add_product_controller()

@app.put('/products/<int:id>')
@jwt_required()
def update(id):
    return update_product_controller(id)


@app.delete('/products/<int:id>')
@jwt_required()
def delete(id):
    return delete_product_controller(id)

# IMAGES

@app.get('/products/<int:product_id>/images')
def product_images(product_id):
    return all_product_images_controller(product_id)

@app.post('/products/<int:product_id>/images')
@jwt_required()
def upload_image(product_id):
    return upload_image_controller(product_id)

@app.delete('/products/<int:product_id>/images/<int:id>')
@jwt_required()
def delete_image(product_id,id):
   return delete_image_by_id_controller(product_id,id)

@app.delete('/products/<int:product_id>/images')
@jwt_required()
def delete_images(product_id):
    return delete_images_by_product_id_controller(product_id)

# CATEGORIES

@app.get('/categories')
def get_all_categories():
    return get_categories_controller()

@app.get('/categories/<int:category_id>/products')
def products_by_category(category_id):
    return get_products_by_category_controller(category_id) 

@app.get('/categories/<int:id>')     
def get_category_by_id(id):
    return get_category_controller(id)

@app.post('/categories')
@jwt_required()
def add_category():
    return add_category_controller()

@app.put('/categories/<int:id>')
@jwt_required()
def update_category_by_id(id):
    return update_category_controller(id)

@app.delete('/categories/<int:id>')
@jwt_required()
def delete_category_by_id(id):
    return delete_category_controller(id)

# CARTS
@app.get('/carts')
@jwt_required()
def get_user_carts():
    return get_carts_user_controller()

@app.post('/carts')
@jwt_required()
def add_user_carts():
    return add_carts_user_controller()

@app.delete('/carts')
@jwt_required()
def delete_user_carts():
    return delete_cart_by_user_id_controller()

@app.delete('/carts/<int:product_id>')
@jwt_required()
def delete_one_user_cart(product_id):
    return delete_cart_by_user_id_and_product_id_controller(product_id)

# TRANSACTIONS

@app.get('/transactions')
@jwt_required()
def get_user_transactions():
    return get_all_user_transactions_controller()

@app.post('/transactions')
@jwt_required()
def add_user_transactions():
    return add_user_transactions_controller()

@app.post('/transactions/carts')
@jwt_required()
def add_user_transaction_from_carts():
    return add_transaction_from_carts_controller()

@app.delete('/transactions')
@jwt_required()
def delete_user_transaction():
    return delete_user_transaction_controller()

# TRANSACTION DETAILS

@app.get('/transactions/<int:transaction_id>/details')
def get_details_by_transaction_id(transaction_id):
    return get_transaction_details_by_transaction_id_controller(transaction_id)

@app.post('/transactions/<int:transaction_id>/details')
def add_transaction_detail(transaction_id):
    return add_transaction_details_contoller(transaction_id)



if __name__==('__main__'):
   app.run(debug=True,port=5001,use_reloader=True,host="0.0.0.0")