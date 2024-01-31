from flask import Flask, render_template
from controllers import *
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
)
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_bcrypt import Bcrypt 



app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app) 
app.config["JWT_SECRET_KEY"] = "bacotttttttt"
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/static/openapi-4.json"  # Our API url (can of course be a local resource)
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={"app_name": "Test application"},  # Swagger UI config overrides
)
app.register_blueprint(swaggerui_blueprint)

# LOGIN AND REGISTER

@app.get("/protected")
@jwt_required()
def get_all_products():
    """
    Retrieves all products, requires authentication.

    Returns:
        dict: Dictionary containing product data.
    """
    return protected_controller()


@app.post("/login")
def get_email_password():
    """
    Logs in the user with provided email and password.

    Returns:
        dict: Dictionary containing a JWT token if login successful.
    """
    return get_email_password_controller()

# USER

@app.post("/register")
def register():
    """
    Registers a new user.

    Returns:
        dict: Dictionary containing a success message if registration successful.
    """
    return register_controller()

@app.get("/users")
@jwt_required()
def get_all_user_data():
    """
    Retrieves all user data, requires authentication.

    Returns:
        dict: Dictionary containing user data.
    """
    return get_user_data_controller()

@app.put("/users")
@jwt_required()
def update_data_user_id():
    """
    Updates user data based on user ID, requires authentication.

    Returns:
        dict: Dictionary containing a success message if update successful.
    """
    return update_data_user_controller()

@app.delete("/users")
@jwt_required()
def delete_user_id():
    """
    Deletes a user based on user ID, requires authentication.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_user_controller()

# ADMIN

@app.post("/admin/register")
def register_admin():
    """
    Registers a new admin.

    Returns:
        dict: Dictionary containing a success message if registration successful.
    """
    return register_admin_controller()

@app.get('/admin')
@jwt_required()
def get_admin_data():
    """
    Retrieves admin data, requires authentication.

    Returns:
        dict: Dictionary containing admin data.
    """
    return get_admin_data_controller()

@app.put("/admin")
@jwt_required()
def update_data_admin_id():
    """
    Updates admin data based on admin ID, requires authentication.

    Returns:
        dict: Dictionary containing a success message if update successful.
    """
    return update_data_admin_controller()

@app.delete("/admin")
@jwt_required()
def delete_admin_id():
    """
    Deletes an admin based on admin ID, requires authentication.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_admin_controller()


# PRODUCTS

@app.get("/products")
def get_products():
    """
    Retrieves all products.

    Returns:
        dict: Dictionary containing product data.
    """
    return get_all_products_controller()


@app.get("/products/<int:id>")
def products_by_id(id):
    """
    Retrieves product by ID.

    Parameters:
        id (int): The ID of the product.

    Returns:
        dict: Dictionary containing product data.
    """
    return get_product_by_id_controller(id)


@app.post("/products")
@jwt_required()
def upload():
    """
    Adds a new product.

    Returns:
        dict: Dictionary containing a success message if addition successful.
    """
    return add_product_controller()


@app.put("/products/<int:id>")
@jwt_required()
def update(id):
    """
    Updates product by ID.

    Parameters:
        id (int): The ID of the product to update.

    Returns:
        dict: Dictionary containing a success message if update successful.
    """
    return update_product_controller(id)


@app.delete("/products/<int:id>")
@jwt_required()
def delete(id):
    """
    Deletes product by ID.

    Parameters:
        id (int): The ID of the product to delete.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_product_controller(id)


# IMAGES

@app.get("/products/<int:product_id>/images")
def product_images(product_id):
    """
    Retrieves all images of a product.

    Parameters:
        product_id (int): The ID of the product.

    Returns:
        dict: Dictionary containing image data.
    """
    return all_product_images_controller(product_id)


@app.post("/products/<int:product_id>/images")
@jwt_required()
def upload_image(product_id):
    """
    Uploads images for a product.

    Parameters:
        product_id (int): The ID of the product.

    Returns:
        dict: Dictionary containing a success message if upload successful.
    """
    return upload_image_controller(product_id)


@app.get("/products/<int:product_id>/images/<int:image_id>")
def get_image(product_id, image_id):
    """
    Retrieves an image of a product by image ID.

    Parameters:
        product_id (int): The ID of the product.
        image_id (int): The ID of the image.

    Returns:
        dict: Dictionary containing image data.
    """
    return get_image_by_id_controller(product_id, image_id)

@app.delete("/products/<int:product_id>/images/<int:image_id>")
@jwt_required()
def delete_image(product_id, image_id):
    """
    Deletes an image of a product by image ID.

    Parameters:
        product_id (int): The ID of the product.
        image_id (int): The ID of the image.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_image_by_id_controller(product_id, image_id)


@app.delete("/products/<int:product_id>/images")
@jwt_required()
def delete_images(product_id):
    """
    Deletes all images of a product.

    Parameters:
        product_id (int): The ID of the product.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_images_by_product_id_controller(product_id)



# CATEGORIES

@app.get("/categories")
def get_all_categories():
    """
    Retrieves all categories.

    Returns:
        dict: Dictionary containing category data.
    """
    return get_categories_controller()


@app.get("/categories/<int:category_id>/products")
def products_by_category(category_id):
    """
    Retrieves products by category ID.

    Parameters:
        category_id (int): The ID of the category.

    Returns:
        dict: Dictionary containing product data.
    """
    return get_products_by_category_controller(category_id)


@app.get("/categories/<int:id>")
def get_category_by_id(id):
    """
    Retrieves category by ID.

    Parameters:
        id (int): The ID of the category.

    Returns:
        dict: Dictionary containing category data.
    """
    return get_category_controller(id)


@app.post("/categories")
@jwt_required()
def add_category():
    """
    Adds a new category.

    Returns:
        dict: Dictionary containing a success message if addition successful.
    """
    return add_category_controller()


@app.put("/categories/<int:id>")
@jwt_required()
def update_category_by_id(id):
    """
    Updates category by ID.

    Parameters:
        id (int): The ID of the category to update.

    Returns:
        dict: Dictionary containing a success message if update successful.
    """
    return update_category_controller(id)


@app.delete("/categories/<int:id>")
@jwt_required()
def delete_category_by_id(id):
    """
    Deletes category by ID.

    Parameters:
        id (int): The ID of the category to delete.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_category_controller(id)



# CARTS

@app.get("/carts")
@jwt_required()
def get_user_carts():
    """
    Retrieves carts belonging to the user.

    Returns:
        dict: Dictionary containing cart data.
    """
    return get_carts_user_controller()


@app.post("/carts")
@jwt_required()
def add_user_carts():
    """
    Adds carts for the user.

    Returns:
        dict: Dictionary containing a success message if addition successful.
    """
    return add_carts_user_controller()


@app.delete("/carts")
@jwt_required()
def delete_user_carts():
    """
    Deletes all carts belonging to the user.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_cart_by_user_id_controller()


@app.delete("/carts/<int:cart_id>")
@jwt_required()
def delete_one_user_cart(cart_id):
    """
    Deletes a specific cart belonging to the user by cart ID.

    Parameters:
        cart_id (int): The ID of the cart to delete.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_cart_by_cart_id_and_user_id_controller(cart_id)



# TRANSACTIONS

@app.get("/transactions")
@jwt_required()
def get_user_transactions():
    """
    Retrieves transactions belonging to the user.

    Returns:
        dict: Dictionary containing transaction data.
    """
    return get_all_user_transactions_controller()

@app.post("/transactions/carts")
@jwt_required()
def add_user_transaction_from_carts():
    """
    Adds a transaction for the user based on their cart contents.

    Returns:
        dict: Dictionary containing a success message if addition successful.
    """
    return add_transaction_from_carts_controller()

@app.post("/transactions")
@jwt_required()
def add_user_transactions():
    """
    Adds transactions for the user.

    Returns:
        dict: Dictionary containing a success message if addition successful.
    """
    return add_user_transactions_controller()
 
@app.delete("/transactions")
@jwt_required()
def delete_user_transaction():
    """
    Deletes all transactions belonging to the user.

    Returns:
        dict: Dictionary containing a success message if deletion successful.
    """
    return delete_user_transaction_controller()


# TRANSACTION DETAILS


@app.get("/transactions/<int:transaction_id>/details")
def get_details_by_transaction_id(transaction_id):
    """
    Retrieves transaction details by transaction ID.

    Parameters:
        transaction_id (int): The ID of the transaction.

    Returns:
        dict: Dictionary containing transaction details.
    """
    return get_transaction_details_by_transaction_id_controller(transaction_id)



if __name__ == ("__main__"):
    app.run(debug=True, port=5001, use_reloader=True, host="0.0.0.0")
