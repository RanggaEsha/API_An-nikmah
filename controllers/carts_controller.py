from models import *
from flask import request

def get_carts_user_controller(user_id):
    if get_user_id(user_id) is None:
        return {"message": "ID user tidak ditemukan"}
    if get_carts_by_user_id(user_id) is None:
        return {"message":"Keranjang user kosong"}
    return get_carts_by_user_id(user_id)

def add_carts_user_controller():
    user_id = request.form.get("user_id")
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    print(user_id)
    print(get_carts_by_user_id(user_id))
    return "",200
    
    # print(data)


    if not get_user_id(user_id):
        return {"message": "ID user tidak ditemukan"}
    if not get_products_by_id(product_id):
        return {"message": "ID produk tidak ditemukan"}
    
    if  get_carts_by_user_id(user_id)["user_id"]!=user_id and get_carts_by_user_id(user_id)["product_id"]!=product_id:
        update_cart(user_id,product_id,quantity)
        result = {"message":"quantity berhasil diubah"}
        return result
    else :
        add_carts(user_id,product_id,quantity)
        result = {"message":"berhasil ditambahkan"}
        return result
    