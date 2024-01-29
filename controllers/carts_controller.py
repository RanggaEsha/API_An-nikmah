from models import *
from errors import *
from flask import request
from flask_jwt_extended import get_jwt_identity


def get_carts_user_controller():
    limit = request.args.get('limit',5)
    page = request.args.get('page',1)
    max_date = request.args.get('max_date')
    min_date = request.args.get('min_date')
    if get_jwt_identity()['role'] == 'admin':
        return get_all_carts(page,limit,max_date,min_date)
    user_id = get_jwt_identity()["id"]
    if not get_carts_by_user_id(user_id,page,limit,max_date,min_date):
        return {"message": "Keranjang belanja anda masih kosong", "data" : []}, 404
    return get_carts_by_user_id(user_id,page,limit,max_date,min_date)

def add_carts_user_controller():
    try:
        user_id = get_jwt_identity()["id"]
        product_id = int(request.form.get("product_id"))
        quantity = request.form.get("quantity")
        product = get_product_by_id(product_id)
        if product is None:
            return {"message": "ID produk tidak ditemukan"}, 404
        if product['quantity'] < int(quantity):
            raise DatabaseError(f"Stok dari produk dengan ID {product_id} hanya tesisa {product['quantity']} barang")
        if get_carts_by_user_id_and_product_id(user_id, product_id) is None:
            add_carts(user_id, product_id, quantity)
            result = {"message": "berhasil ditambahkan"}, 200
            return result
        else:
            update_cart(product_id, user_id, quantity)
            result = {"message": "quantity berhasil diubah"}, 200
            return result
    except ValueError as ve:
        return {"message": str(ve)},422
    except DatabaseError as e:
        return {"message": str(e)},404
    except Exception as e:
        return {"message": str(e)},422

def delete_cart_by_user_id_controller():
    try:
        user_id = get_jwt_identity()["id"]
        delete_cart_by_user_id(user_id)
        return {"message": "berhasil menghapus semua keranjang anda"}
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422

def delete_cart_by_cart_id_and_user_id_controller(cart_id):
    try:
        user_id = get_jwt_identity()["id"]
        if get_cart_by_cart_id_and_user_id(cart_id,user_id) is None:
            raise DatabaseError("ID keranjang anda tidak ditemukan")
        delete_cart_by_user_id_and_cart_id(cart_id, user_id)
        return {"message": "berhasil menghapus keranjang"}
    except DatabaseError as e:
        return {"message": str(e)},404
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422
