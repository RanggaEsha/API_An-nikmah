from flask import request 
from models import *
import time, os

def get_all_products_controller():
    limit = int(request.args.get("limit",5))
    page = int(request.args.get("page",1))
    category = request.args.get("category")
    keyword = request.args.get("keyword")
    max_price = request.args.get("max_price")
    min_price = request.args.get("min_price")

    return get_all_products(page=page,limit=limit,category=category,keyword=keyword,max_price=max_price,min_price=min_price)

def get_products_by_category_controller(category_id):
    if get_products_by_category(category_id) is None:
        return {"message":"kategori id tidak ditemukan."},402
    return get_products_by_category(category_id)

def get_products_by_id_controller(id):
    if not id or id == '':
        return {"message":"ID produk harus diisi."},402
    if get_products_by_id(id) is None:
        return {"message":"ID produk tidak ditemukan."},402
    images = all_product_images(id)
    product = get_products_by_id(id)
    product["images"]= images
    return product
    

def add_product_controller():
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

    if not name or not description or not price or not quantity or not category_id:
        return {"message":"Semua inputan harus diisi."},402

    locations = []
    for file in files:
        location = "static/uploads/" + str(time.time()) + "_" + file.filename
        file.save(location)
        locations.append(location)
    try:
        
        last_inserted_id = upload_product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
        )
        upload_product_images(locations,last_inserted_id)

    except Exception as e:
        for file in locations:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "upload produk berhasil"},200

def update_product_controller(product_id):
    if get_products_by_id(product_id) is None:
        return {"message": "ID produk tidak ditemukan"},404
    name = request.form.get("name")
    description = request.form.get("description")
    price = int(request.form.get("price"))
    quantity = int(request.form.get("quantity"))
    category_id = int(request.form.get("category_id"))

    if not name or not description or not price or not quantity or not category_id:
        return {"message":"Semua inputan harus diisi."},402

    if 'file' not in request.files:
        try:
            update_product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,

        )
            return {'message':'Product updated successfully'},200
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

    try:
        images = all_product_images(product_id=product_id)
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
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "update produk berhasil"},200


def delete_product_controller(product_id: int):
    if get_products_by_id(product_id): 
        images = all_product_images(product_id=product_id)
        delete_product(product_id)
        for image in images:
            if os.path.exists(image["image"]):
                os.remove(image["image"])
        return {"message": "berhasil menghapus produk"},200
    return {"message": "ID produk tidak ditemukan"},404

# PRODUCT IMAGES MODELS

def all_product_images_controller(product_id):
    if get_products_by_id(product_id) is None:
        return {"message": "ID produk tidak ditemukan"}, 404
    all_product_images(product_id)


def upload_image_controller():
    if "file" not in request.files:
        return "no file part"

    files = request.files.getlist("file")

    # Check if the file is selected
    if not files:
        return "No selected files"

    allowed_files = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
    # Check if the file type is allowed
    for file in files:
        if file.content_type not in allowed_files:
            return "File type not allowed"

    # Save the uploaded file to a specific folder
    locations = []
    for file in files:
        location = "static/uploads/" + str(time.time()) + "_" + file.filename
        file.save(location)
        locations.append(location)

    product_id = request.form.get("product_id")

    if not product_id or product_id == "":
        return {"message": "tambahkan ID produk"}

    if get_products_by_id(product_id) is None:
        return {"message": "ID produk tidak ditemukan"}, 404

    try:
        upload_product_images(image_location=locations, product_id=product_id)
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "upload produk berhasil"}, 200


def delete_image_by_id_controller(product_id,id):
    if get_products_by_id(product_id) is None:
        return {"message": "ID produk tidak ditemukan"}, 404
    if all_product_images(id) is None:
        return {"message": "ID image tidak ditemukan"}, 404
    image = get_product_image_by_id(id)
    # return image
    if os.path.exists(image["image"]):
            os.remove(image["image"])
    delete_image_by_id(id)
    return {"message": "image berhasil dihapus"}, 200

def delete_images_by_product_id_controller(product_id):
    if all_product_images(product_id) is None:
        return {"message": "Product ID image tidak ditemukan"}, 404
    images = all_product_images(product_id=product_id)
    delete_images_by_product_id(product_id)
    # membersihkan data gambar yang lama
    for image in images:
        if os.path.exists(image["image"]):
            os.remove(image["image"])

    return {"message": "image berhasil dihapus"}, 200
