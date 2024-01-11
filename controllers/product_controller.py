from flask import request
from models import product
import time, os


def add_product():
    # Check if 'file' is in request.files
    if "file" not in request.files:
        return "no file part"

    file = request.files["file"]

    # Check if the file is selected
    if file.filename == "":
        return "No selected file"

    # Check if the file type is allowed
    if file.content_type not in ["image/jpeg", "image/jpg", "image/webp", "image/png"]:
        return "File type not allowed"

    # Save the uploaded file to a specific folder
    location = "static/uploads/" + str(time.time()) + "_" + file.filename
    file.save(location)

    # product_id = request.form.get('product_id')
    name = request.form.get("name")
    description = request.form.get("description")

    price = int(request.form.get("price"))
    quantity = int(request.form.get("quantity"))
    created_at = request.form.get("created_at")
    category_id = int(request.form.get("category_id"))

    try:
        product.upload_product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            created_at=created_at,
            category_id=category_id,
            image_location=location,
        )
    except Exception as e:
        if os.path.exists(location):
            os.remove(location)
        raise e
    return {"message": "upload produk berhasil"}
