from models import *
from flask import request
from flask_jwt_extended import get_jwt_identity

def get_all_user_transactions_controller():
    user_id = get_jwt_identity()["id"]
    print(user_id)
    print("hallo", get_transactions_by_user_id(user_id))
    if get_transactions_by_user_id(user_id) is None:
        return {"message": "transaksi anda masih kosong"}, 404
    return get_transactions_by_user_id(user_id)

def add_user_transactions_controller():
    user_id = get_jwt_identity()["id"]
    address = request.form.get("address")
    fullname = request.form.get("fullname")
    phone_number = request.form.get("phone_number")
    product_ids = request.form.getlist("product_id")
    quantities = request.form.getlist("quantity")
    if not address or not fullname or not phone_number:
        return {"message":"isi data diri anda dengan benar"},404
    if not product_ids or not quantities:
        return {"message":"pastikan produk anda sesuai atau tidak kosong"},404
    try:
            transaction = add_transaction(user_id,address,fullname,phone_number)
            for i in range(len(product_ids)):
                product_id = product_ids[i]
                quantity = int(quantities[i])
                products = get_products_by_id(product_id)
                if int(products["quantity"]) < quantity:
                    delete_transaction_by_id(transaction)
                    return {"message": f"Stok dari {products['name']} hanya tesisa {products['quantity']} barang"}, 404
                total = products["price"] * quantity
                add_transaction_details(transaction, product_id, quantity, total)
                updated_quantity = products['quantity'] - quantity
                update_product_quantity(product_id,updated_quantity)
    except Exception as e:
        raise e
    return {"message": "berhasil ditambahkan"},200

def add_transaction_from_carts_controller():
    user_id = get_jwt_identity()["id"]
    address = request.form.get("address")
    fullname = request.form.get("fullname")
    phone_number = request.form.get("phone_number")
    if not address or not fullname or not phone_number:
        return {"message":"isi data diri anda dengan benar"},404
    
 
    try :
        transaction = add_transaction(user_id,address,fullname,phone_number)
        for i in range(len(get_carts_by_user_id(user_id))):
            product = get_carts_by_user_id(user_id)[i]["product_id"]
            quantity = int(get_carts_by_user_id(user_id)[i]["quantity"])
            products = get_products_by_id(product)
            if int(products["quantity"]) < quantity:
                delete_transaction_by_id(transaction)
                return {"message": f"Stok dari {products['name']} hanya tesisa {products['quantity']} barang"}, 404
            total = products["price"] * quantity
            add_transaction_details(transaction, product, quantity, total)
            updated_quantity = products['quantity'] - quantity
            update_product_quantity(product,updated_quantity)
            
    except Exception as e:
        raise e
    return {"message": "berhasil ditambahkan"},200

def delete_user_transaction_controller():
    user_id = get_jwt_identity()["id"]
    delete_transaction_by_id(user_id)
    return {"message": "berhasil dihapus"},200

# TRANSACTION DETAILS

def get_transaction_details_by_transaction_id_controller(transaction_id):
    print(transaction_id)
    print(get_transactions_by_id(transaction_id))
    if get_transactions_by_id(transaction_id) is None:
        return {"message": "transaksi anda masih kosong"}, 404
    if get_transaction_details_by_transaction_id(transaction_id):
        return get_transaction_details_by_transaction_id(transaction_id)
    return {"message": "transaksi anda masih kosong"}, 404
def add_transaction_details_contoller(transaction_id):
    if get_transactions_by_id(transaction_id) is None:
        return {"message": "transaksi anda masih kosong"}, 404
    
    
    
