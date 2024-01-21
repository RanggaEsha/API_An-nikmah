from models import *
from flask import request
from flask_jwt_extended import get_jwt_identity


def get_carts_user_controller():
    user_id = get_jwt_identity()["id"]
    if not get_carts_by_user_id(user_id):
        return {"message": "Keranjang belanja anda masih kosong"}, 404
    return get_carts_by_user_id(user_id)

def add_carts_user_controller():
    user_id = get_jwt_identity()["id"]
    product_id = int(request.form.get("product_id"))
    quantity = request.form.get("quantity")
    if get_products_by_id(product_id) is None:
        return {"message": "ID produk tidak ditemukan"},404
    
    if get_carts_by_user_id_and_product_id(user_id,product_id) is None:
        add_carts(user_id, product_id, quantity)
        result = {"message": "berhasil ditambahkan"},200
        return result
    
    else:
        update_cart(product_id, user_id, quantity)
        result = {"message": "quantity berhasil diubah"},200
        return result
    
def delete_cart_by_user_id_controller():
    user_id = get_jwt_identity()["id"]
    delete_cart_by_user_id(user_id)
    return {"message": "berhasil menghapus semua keranjang anda"}

def delete_cart_by_user_id_and_product_id_controller(product_id):
    user_id = get_jwt_identity()["id"]
    delete_cart_by_user_id_and_product_id(user_id,product_id)
    return {"message": "berhasil menghapus keranjang"}


