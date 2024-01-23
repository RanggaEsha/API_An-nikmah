from models import *
from flask import request
from flask_jwt_extended import get_jwt_identity
from errors import OutOfStockError


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
                return {"message": f"Produk dengan ID {product_id} sedang kosong"}, 404
            if int(products["quantity"]) < quantity:
                return {
                    "message": f"Stok dari produk dengan ID {product_id} hanya tesisa {products['quantity']} barang"
                }, 404
            total = products["price"] * quantity
            add_transaction_details(transaction, product_id, quantity, total)
            updated_quantity = products["quantity"] - quantity
            update_product_quantity(product_id, updated_quantity)
        conn.commit()
    except OutOfStockError as os:
        return {"message": str(os)}
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        conn.rollback()
        return {"message": str(e)},422
    finally:
        cur.close()
    return {"message": "berhasil ditambahkan"}, 200


def add_transaction_from_carts_controller():
    user_id = get_jwt_identity()["id"]
    address = request.form.get("address")
    fullname = request.form.get("fullname")
    phone_number = request.form.get("phone_number")
    cart_ids = request.form.getlist("cart_id")
    if not address or not fullname or not phone_number:
        return {"message": "isi data diri anda dengan benar"}, 404

    cur = conn.cursor()
    try:
        # adding data to transactions
        transaction = add_transaction(user_id, address, fullname, phone_number)
        # adding data to transaction details
        for cart_id in cart_ids:
            cart = get_cart_by_id(cart_id)
            product = get_product_by_id(cart["product_id"])
            quantity = int(cart["quantity"])
            if int(product["quantity"]) < quantity:
                raise OutOfStockError(
                    f"Stok dari {product['name']} hanya tesisa {product['quantity']} barang"
                )
            total = product["price"] * quantity
            add_transaction_details(transaction, product["id"], quantity, total)
            updated_quantity = product["quantity"] - quantity
            update_product_quantity(product["id"], updated_quantity)
            delete_cart_by_id(cart_id)
        conn.commit()
        return {"message": "berhasil ditambahkan"}, 200
    except OutOfStockError as e:
        conn.rollback()
        return {"message": e}
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
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        conn.rollback()
        return {"message": str(e)},422

# TRANSACTION DETAILS


def get_transaction_details_by_transaction_id_controller(transaction_id):
    if get_transactions_by_id(transaction_id) is None:
        return {"message": "transaksi anda masih kosong"}, 404
    if get_transaction_details_by_transaction_id(transaction_id):
        return get_transaction_details_by_transaction_id(transaction_id)
    return {"message": "transaksi anda masih kosong"}, 404
