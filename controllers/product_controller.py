from flask import request
from models import *
import time, os
from flask_jwt_extended import get_jwt_identity


def get_all_products_controller():
    """
    Controller function to retrieve a list of products based on specified parameters.

    Query Parameters:
    - limit (int, optional): The number of products to retrieve per page (default: 5).
    - page (int, optional): The page number for pagination (default: 1).
    - category (str, optional): The category name for filtering products.
    - keyword (str, optional): The keyword to search for in product names.
    - max_price (int, optional): The maximum price for filtering products.
    - min_price (int, optional): The minimum price for filtering products.

    Returns:
    - dict or tuple: A dictionary containing the list of products or an error message with status code.
      If products are found, the dictionary contains the "products" key with the list of products.
      If no products are found, the dictionary contains nothing or [].
    """
    limit = int(request.args.get("limit", 5))
    page = int(request.args.get("page", 1))
    category = request.args.get("category")
    keyword = request.args.get("keyword")
    max_price = request.args.get("max_price")
    min_price = request.args.get("min_price")
    if get_category_name(category):
        return {"message": "Kategori ID tidak ditemukan."}, 404
    data = get_all_products(
        page=page,
        limit=limit,
        category=category,
        keyword=keyword,
        max_price=max_price,
        min_price=min_price,
    )
    return data


def get_products_by_category_controller(category_id: int):
    """
    Controller function to retrieve a list of products based on a specified category ID.

    Parameters:
    - category_id (int): The ID of the category for which products are to be retrieved.

    Returns:
    - dict or tuple: A dictionary containing the category information and the list of products or an error message with status code.
      If the category ID is not found, the dictionary contains a "message" key with an error message and a 404 status code.
      If products are found, the dictionary contains the "category" key with the category information and the "products" key with the list of products.
      If no products are found, the "products" key contains a If no products are found, the dictionary contains nothing or [].
    """
    if get_products_by_category(category_id) is None:
        return {"message": "kategori id tidak ditemukan."}, 404
    products = get_products_by_category(category_id)
    category = get_category(category_id)
    category["products"] = products
    return category


def get_product_by_id_controller(id: int):
    """
    Controller function to retrieve a product based on a specified product ID.

    Parameters:
    - id (int): The ID of the product to be retrieved.

    Returns:
    - dict or tuple: A dictionary containing the product information or an error message with status code.
      If the product ID is not provided or is empty, the dictionary contains a "message" key with an error message and a 404 status code.
      If the product ID is not found, the dictionary contains a "message" key with an error message and a 404 status code.
      If the product is found, the dictionary contains the product information.
    """
    if not id or id == "":
        return {"message": "ID produk harus diisi."}, 404
    product = get_product_by_id(id)
    if product is None:
        return {"message": "ID produk tidak ditemukan."}, 404
    return product


def add_product_controller():
    """
    Controller function to add a new product.

    Returns:
    - dict or tuple: A dictionary containing success message or an error message with status code.
      If the user is not authorized (not an admin), the dictionary contains a "message" key with an "Unauthorized" message and a 403 status code.
      If no file is provided, the dictionary contains a "message" key with a "no file part" message.
      If no selected files are provided, the dictionary contains a "message" key with a "No selected files" message.
      If the file type is not allowed, the dictionary contains a "message" key with a "File type not allowed" message.
      If the category ID is not found, the dictionary contains a "message" key with a "Kategori ID tidak ditemukan." message and a 404 status code.
      If any required input is missing, the dictionary contains a "message" key with a "Semua inputan harus diisi." message and a 402 status code.
      If the product and image upload is successful, the dictionary contains a "message" key with an "upload produk berhasil" message and a 200 status code.
    """
    
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 403
        if "file" not in request.files:
            return "no file part"
        files = request.files.getlist("file")
        if not files:
            return "No selected files"
        allowed_files = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
        for file in files:
            if file.content_type not in allowed_files:
                return "File type not allowed"

        name = request.form.get("name")
        description = request.form.get("description")
        price = int(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        category_id = int(request.form.get("category_id"))
        if not get_category(category_id):
            return {"message": "Kategori ID tidak ditemukan."}, 404
        if not name or not description or not price or not quantity or not category_id:
            return {"message": "Semua inputan harus diisi."}, 402

        locations = []
        for file in files:
            location = "static/uploads/" + str(time.time()) + "_" + file.filename
            file.save(location)
            locations.append(location)
            last_inserted_id = upload_product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                category_id=category_id,
            )
            upload_product_images(locations, last_inserted_id)
    except ValueError as ve:
        return {"message": str(ve)}
    
    except Exception as e:
        for file in locations:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "upload produk berhasil"}, 200


def update_product_controller(product_id: int):
    """
    Controller function to update an existing product.

    Parameters:
    - product_id (int): The ID of the product to be updated.

    Returns:
    - dict or tuple: A dictionary containing success message or an error message with status code.
      If the user is not authorized (not an admin), the dictionary contains a "message" key with an "Unauthorized" message and a 403 status code.
      If the product ID is not found, the dictionary contains a "message" key with an "ID produk tidak ditemukan" message and a 404 status code.
      If any required input is missing, the dictionary contains a "message" key with a "Semua inputan harus diisi." message and a 402 status code.
      If the product is updated successfully, the dictionary contains a "message" key with a "Product updated successfully" message and a 200 status code.
      If no files are provided, the dictionary contains a "message" key with a "No selected files" message and a 400 status code.
      If the file type is not allowed, the dictionary contains a "message" key with a "File type not allowed for file: %s" message and a 400 status code.
      If there is an error during the update, the dictionary contains a "message" key with an "update produk berhasil" message and a 200 status code.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 401
        if get_product_by_id(product_id) is None:
            return {"message": "ID produk tidak ditemukan"}, 404
        name = request.form.get("name")
        description = request.form.get("description")
        price = int(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        category_id = int(request.form.get("category_id"))

        if not name or not description or not price or not quantity or not category_id:
            return {"message": "Semua inputan harus diisi."}, 402

        if "file" not in request.files:
            try:
                update_product(
                    product_id=product_id,
                    name=name,
                    description=description,
                    price=price,
                    quantity=quantity,
                    category_id=category_id,
                )
                return {"message": "Product updated successfully"}, 200
            except Exception as e:
                raise e
        files = request.files.getlist("file")
        if not files:
            return "No selected files", 400
        allowed_file_types = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
        for file in files:
            if file.content_type not in allowed_file_types:
                return "File type not allowed for file: %s" % file.filename, 400

        locations = []
        for file in files:
            location = "static/uploads/" + str(time.time()) + "_" + file.filename
            file.save(location)
            locations.append(location)

    
        images = get_all_product_images(product_id=product_id)
        update_product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
            image_location=locations,
        )
        for image in images:
            if os.path.exists(image["image"]):
                os.remove(image["image"])
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "update produk berhasil"}, 200


def delete_product_controller(product_id: int):
    """
    Controller function to delete a product.

    Parameters:
    - product_id (int): The ID of the product to be deleted.

    Returns:
    - dict or tuple: A dictionary containing success message or an error message with status code.
      If the user is not authorized (not an admin), the dictionary contains a "message" key with an "Unauthorized" message and a 403 status code.
      If the product ID is not found, the dictionary contains a "message" key with an "ID produk tidak ditemukan" message and a 404 status code.
      If the product is deleted successfully, the dictionary contains a "message" key with a "berhasil menghapus produk" message and a 200 status code.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 403
        if get_product_by_id(product_id):
            images = get_all_product_images(product_id=product_id)
            delete_product(product_id)
            for image in images:
                if os.path.exists(image["image"]):
                    os.remove(image["image"])
            return {"message": "berhasil menghapus produk"}, 200
        return {"message": "ID produk tidak ditemukan"}, 404
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422

# PRODUCT IMAGES MODELS


def all_product_images_controller(product_id: int):
    """
    Controller function to retrieve all images associated with a specific product.

    Parameters:
    - product_id (int): The ID of the product for which images are to be retrieved.

    Returns:
    - dict or tuple: A dictionary containing the product information and a list of images or an error message with status code.
      If the product ID is not found, the dictionary contains a "message" key with an "ID produk tidak ditemukan" message and a 404 status code.
      If images are found, the dictionary contains the product information and an "images" key with the list of images.
      If no images are found, the "images" key contains a message indicating that there are no images for the product.
    """
    try:
        if get_product_by_id(product_id) is None:
            return {"message": "ID produk tidak ditemukan"}, 404
        images = get_all_product_images(product_id)
        product = get_product_by_id(product_id)
        product["images"] = images
        return product
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422

def upload_image_controller(product_id: int):
    """
    Controller function to upload images for a specific product.

    Parameters:
    - product_id (int): The ID of the product for which images are to be uploaded.

    Returns:
    - dict or tuple: A dictionary containing success message or an error message with status code.
      If the user is not authorized (not an admin), the dictionary contains a "message" key with an "Unauthorized" message and a 403 status code.
      If no file is provided, the dictionary contains a "message" key with a "no file part" message.
      If no selected files are provided, the dictionary contains a "message" key with a "No selected files" message.
      If the file type is not allowed, the dictionary contains a "message" key with a "File type not allowed" message.
      If no product ID is provided or it is empty, the dictionary contains a "message" key with a "tambahkan ID produk" message.
      If the product ID is not found, the dictionary contains a "message" key with an "ID produk tidak ditemukan" message and a 404 status code.
      If the image upload is successful, the dictionary contains a "message" key with an "upload produk berhasil" message and a 200 status code.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 401
        if "file" not in request.files:
            return "no file part"

        files = request.files.getlist("file")

        if not files:
            return "No selected files"

        allowed_files = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
        for file in files:
            if file.content_type not in allowed_files:
                return "File type not allowed"

        locations = []
        for file in files:
            location = "static/uploads/" + str(time.time()) + "_" + file.filename
            file.save(location)
            locations.append(location)
        if not product_id or product_id == "":
            return {"message": "tambahkan ID produk"}

        if get_product_by_id(product_id) is None:
            return {"message": "ID produk tidak ditemukan"}, 404
        upload_product_images(image_location=locations, product_id=product_id)
        return {"message": "upload produk berhasil"}, 200
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise {"message": str(e)}
    


def delete_image_by_id_controller(product_id: int, image_id: int):
    """
    Controller function to delete a specific image associated with a product.

    Parameters:
    - product_id (int): The ID of the product to which the image belongs.
    - id (int): The ID of the image to be deleted.

    Returns:
    - dict or tuple: A dictionary containing success message or an error message with status code.
      If the user is not authorized (not an admin), the dictionary contains a "message" key with an "Unauthorized" message and a 403 status code.
      If the product ID is not found, the dictionary contains a "message" key with an "ID produk tidak ditemukan" message and a 404 status code.
      If the image ID is not found, the dictionary contains a "message" key with an "ID image tidak ditemukan" message and a 404 status code.
      If the image is deleted successfully, the dictionary contains a "message" key with an "image berhasil dihapus" message and a 200 status code.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 401
        if get_product_by_id(product_id) is None:
            return {"message": "ID produk tidak ditemukan"}, 404
        if get_all_product_images(id) is None:
            return {"message": "ID image tidak ditemukan"}, 404
        image = get_product_image_by_id(image_id)
        if os.path.exists(image["image"]):
            os.remove(image["image"])
        delete_image_by_id(id)
        return {"message": "image berhasil dihapus"}, 200
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422

def delete_images_by_product_id_controller(product_id):
    """
    Controller function to delete all images associated with a specific product.

    Parameters:
    - product_id (int): The ID of the product for which images are to be deleted.

    Returns:
    - dict or tuple: A dictionary containing success message or an error message with status code.
      If the user is not authorized (not an admin), the dictionary contains a "message" key with an "Unauthorized" message and a 403 status code.
      If no images are found for the provided product ID, the dictionary contains a "message" key with a "Product ID image tidak ditemukan" message and a 404 status code.
      If images are found and deleted successfully, the dictionary contains a "message" key with an "image berhasil dihapus" message and a 200 status code.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 401
        if get_all_product_images(product_id) is None:
            return {"message": "Product ID image tidak ditemukan"}, 404
        images = get_all_product_images(product_id=product_id)
        delete_images_by_product_id(product_id)
        for image in images:
            if os.path.exists(image["image"]):
                os.remove(image["image"])
        return {"message": "image berhasil dihapus"}, 200
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422
