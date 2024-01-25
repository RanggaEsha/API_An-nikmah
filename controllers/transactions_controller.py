from models import *
from flask import request
from flask_jwt_extended import get_jwt_identity
from errors import *


def get_all_user_transactions_controller():
    user_id = get_jwt_identity()["id"]
    if get_transactions_by_user_id(user_id) is None:
        return {"message": "transaksi anda masih kosong"}, 404
    return get_transactions_by_user_id(user_id)


def add_user_transactions_controller():
    try:
        user_id = get_jwt_identity()["id"]
        address = request.form.get("address")
        fullname = request.form.get("fullname")
        phone_number = request.form.get("phone_number")
        product_ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        if not address or not fullname or not phone_number:
            return {"message": "isi data diri anda dengan benar"}, 404
        if not product_ids or not quantities:
            return {"message": "pastikan produk anda sesuai atau tidak kosong"}, 404
        cur = conn.cursor()

        # adding data to transactions
        transaction = add_transaction(user_id, address, fullname, phone_number)
        # adding data to transaction details
        for i in range(len(product_ids)):
            product_id = product_ids[i]
            quantity = int(quantities[i])
            products = get_product_by_id(product_id)
            if products is None:
                return DatabaseError(f"Produk dengan ID {product_id} sedang kosong")
            if int(products["quantity"]) < quantity:
                raise DatabaseError(f"Stok dari produk dengan ID {product_id} hanya tesisa {products['quantity']} barang")
            total = products["price"] * quantity
            add_transaction_details(transaction, product_id, quantity, total)
            updated_quantity = products["quantity"] - quantity
            update_product_quantity(product_id, updated_quantity)
        conn.commit()
        return {"message": "berhasil ditambahkan"}, 200
    except DatabaseError as e:
        return {"message": str(e)},404
    except Exception as e:
        conn.rollback()
        return {"message": str(e)}, 422
    finally:
        cur.close()
   


def add_transaction_from_carts_controller():
    cur = conn.cursor()
    try:
        user_id = get_jwt_identity()["id"]
        address = request.form.get("address")
        fullname = request.form.get("fullname")
        phone_number = request.form.get("phone_number")
        cart_ids = request.form.getlist("cart_ids")
        cart_ids = request.form.get("cart_ids")
        # if cart_ids:
        #     cart_ids = cart_ids.split(',')
        if not address or not fullname or not phone_number:
            raise ValueError("isi data diri anda dengan benar")

        
        # adding data to transactions
        transaction = add_transaction(user_id, address, fullname, phone_number)
        # adding data to transaction details
        for cart_id in cart_ids:
            print("ijsdbh", cart_ids)
            cart = get_cart_by_id(cart_id)
            if cart is None:
                raise DatabaseError("Cart kosong")
            print("avdbsjlk", cart["product_id"])
            product = get_product_by_id(cart["product_id"])
            quantity = int(cart["quantity"])
            if int(product["quantity"]) < quantity:
                raise DatabaseError(
                    f"Stok dari product deng ID {product['id']} hanya tesisa {product['quantity']} barang"
                )
            total = product["price"] * quantity
            add_transaction_details(transaction, product["id"], quantity, total)
            updated_quantity = product["quantity"] - quantity
            update_product_quantity(product["id"], updated_quantity)
            delete_cart_by_id(cart_id)
        conn.commit()
        return {"message": "berhasil ditambahkan"}, 200
    except DatabaseError as a:
        conn.rollback() 
        return {"message": str(a)},404
    except ValueError as v:
        conn.rollback() 
        return {"message": str(v)},404
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_user_transaction_controller():
    try:
        user_id = get_jwt_identity()["id"]
        delete_transaction_by_id(user_id)
        return {"message": "berhasil dihapus"}, 200
    except Exception as e:
        conn.rollback()
        return {"message": str(e)}, 422


# TRANSACTION DETAILS


def get_transaction_details_by_transaction_id_controller(transaction_id):
    try:
        if get_transactions_by_id(transaction_id) is None:
            return {"message": "transaksi anda masih kosong"}, 404
        data = get_transaction_details_by_transaction_id(transaction_id)
        if data is not None:
            return get_transaction_details_by_transaction_id(transaction_id)
        return {"message": "detail transaksi anda masih kosong"}, 404
    except DatabaseError as e:
        return {"message": str(e)}, 404
