from flask import request 
from models import *
import time, os

def get_all_products_controller():
    return get_all_products()

def get_products_by_category_controller(category_id):
    
    
    if product_category_id_validator(category_id) is None:
        return {"message":"kategori id tidak ditemukan."},402
    
    return get_products_by_category(category_id)

def get_products_by_id_controller(id):
    if not id or id == '':
        return {"message":"ID produk harus diisi."},402
    
    if product_id_validator(id) is None:
        return {"message":"ID produk tidak ditemukan."},402
    
    return get_products_by_id(id)


def get_products_by_price_range_controller():
    max_price = request.args.get('max_price')
    min_price = request.args.get('min_price')

    if not max_price and not min_price:
        return {"message": "salah satu dari max price atau min price harus diisi."}, 402

    try:
        max_price = int(max_price) if max_price else None
        min_price = int(min_price) if min_price else None
    except ValueError:
        return {"message": "max price dan min price harus berupa angka yang valid."}, 402

    return get_products_by_price_range(max_price, min_price)
    

def add_product_controller():
    # Check if 'file' is in request.files
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

    # product_id = request.form.get('product_id')
    name = request.form.get("name")
    description = request.form.get("description")
    price = int(request.form.get("price"))
    quantity = int(request.form.get("quantity"))
    category_id = int(request.form.get("category_id"))

    if not name or not description or not price or not quantity or not category_id:
        return {"message":"Semua inputan harus diisi."},402

    try:
        upload_product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
            image_location=locations,
        )

    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "upload produk berhasil"},200

def update_product_controller(product_id):

    if product_id_validator(product_id) is None:
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
            image_location=None,
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
        update_product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
            image_location=locations,
        )
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "update produk berhasil"},200


def delete_product_controller(product_id: int):
    if product_id_validator(product_id):   
        delete_product(product_id)
        return {"message": "berhasil menghapus produk"},200
    return {"message": "ID produk tidak ditemukan"},404



