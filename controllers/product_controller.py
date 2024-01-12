from flask import request 
from models import product
import time, os

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

    try:
        product.upload_product(
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
    return {"message": "upload produk berhasil"}
