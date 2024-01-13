from models import *
from flask import request
import time, os

def all_product_images_controller(product_id):
    if product_id_validator(product_id) is None:
        return {"message": "ID produk tidak ditemukan"},404
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

    if not product_id or product_id=="":
        return {"message": "tambahkan ID produk"}
    
    if product_id_validator(product_id=product_id) is None:
        return {"message": "ID produk tidak ditemukan"},404
    
    try:
        upload_product_images(
            image_location=locations,
            product_id=product_id
        )
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "upload produk berhasil"},200

def update_image_controller(id):
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
    if not product_id or product_id=="":
        return {"message": "tambahkan ID produk"}

    if product_id_validator(product_id=product_id) is None:
        return {"message": "ID produk tidak ditemukan"},404

    if image_id_validator(id) is None:
        return {"message": "ID image tidak ditemukan"},404
    
    try:
        update_product_images(
            id,
            image_location=locations,
            product_id=product_id
        )
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "update produk berhasil"},200

        


    
    
