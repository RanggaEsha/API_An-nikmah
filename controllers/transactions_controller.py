from models import *
from flask import request
from flask_jwt_extended import get_jwt_identity
from errors import *
from form_validator import get_transaction_form,add_transaction_form,add_transaction_from_cart_form,validate_date_format


def get_all_user_transactions_controller():
    """
    Controller function to retrieve all transactions for a user.

    Returns:
        dict: A dictionary containing transaction data if successful.
        dict: An error message with a 404 status code if no transactions are found.
    """
    try:
        # Getting query parameters for pagination and date filtering
        limit = request.args.get("limit", 5)
        page = request.args.get("page", 1)
        max_date = request.args.get("max_date")
        min_date = request.args.get("min_date")
         # Check if either max_date or min_date is provided in the request
        if max_date or min_date:

            # Validate format of max_date if it's present
            if max_date and not validate_date_format(max_date):
                # Raise an error with a message about invalid max_date format
                errors = {"max_date": ["Invalid date format. Use YYYY-MM-DD."]}
                raise ValueError(errors)

            # Validate format of min_date if it's present
            if min_date and not validate_date_format(min_date):
                # Raise an error with a message about invalid min_date format
                errors = {"min_date": ["Invalid date format. Use YYYY-MM-DD."]}
                raise ValueError(errors)

            # Create a form instance from request.form data
            form = get_transaction_form(request.form)

            # Perform additional validation on the form
            if not form.validate():
                # Collect errors from the form fields
                errors = {field.name: field.errors for field in form if field.errors}
                # Raise a ValueError with the collected form errors
                raise ValueError(errors)
        
        # Checking if the user is an admin
        if get_jwt_identity()["role"] == "admin":
            # If admin, return all transactions
            return get_all_transactions(limit, page, max_date, min_date)
        
        # If not admin, get user ID from JWT
        user_id = get_jwt_identity()["id"]
        
        # Getting transactions for the specific user
        user_transactions = get_transactions_by_user_id(user_id, limit, page, max_date, min_date)
        
        # Checking if transactions exist for the user
        if user_transactions is None:
            raise DatabaseError("transaksi anda masih kosong")
        
        # Return user transactions if found
        return user_transactions
    except DatabaseError as e:
        # Return error message and an empty data of list if database error occurs
        return {"error": str(e),"data":[]}, 404
    except Exception as e:
        raise e



def add_user_transactions_controller():
    """
    Controller function to add transactions for a user.

    Returns:
        dict: A dictionary containing a success message if the transaction is added successfully.
        dict: An error message with a 404 status code if there are issues with the transaction data.
    """
    cur = conn.cursor()  # Initialize a cursor
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()["id"]
        
        # Retrieve transaction details from form data
        address = request.form.get("address")
        fullname = request.form.get("fullname")
        phone_number = request.form.get("phone_number")
        product_ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        form = add_transaction_form(request.form)
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        
        # Begin a transaction
        transaction = add_transaction(user_id, address, fullname, phone_number)
        
        # Add transaction details for each product
        for i in range(len(product_ids)):
            product_id = product_ids[i]
            quantity = int(quantities[i])
            products = get_product_by_id(product_id)
            
            # Check if the product exists
            if products is None:
                raise DatabaseError(f"Produk dengan ID {product_id} sedang kosong")
            
            # Check if there is enough quantity of the product
            if int(products["quantity"]) < quantity:
                raise DatabaseError(
                    f"Stok dari produk dengan ID {product_id} hanya tersisa {products['quantity']} barang"
                )
            
            # Calculate subtotal and add transaction details
            sub_total = products["price"] * quantity
            product_price = products["price"]
            add_transaction_details(
                transaction, product_id, product_price, quantity, sub_total
            )
            
            # Update the quantity of the product
            updated_quantity = products["quantity"] - quantity
            update_product_quantity(product_id, updated_quantity)
        
        # Commit the transaction
        conn.commit()
        return {"message": "Berhasil ditambahkan"}, 200

    except ValueError as e:
        # Rollback transaction and return error message for value error
        conn.rollback()
        return {"errors": e.args[0]}, 404
    except DatabaseError as e:
        # Rollback transaction and return error message for database error
        conn.rollback()
        return {"error": str(e)}, 404
    except Exception as e:
        # Rollback transaction and raise exception for other errors
        conn.rollback()
        raise e
    finally:
        # Close the cursor
        cur.close()




def add_transaction_from_carts_controller():
    """
    Controller function to add transactions from user's carts.

    Returns:
        dict: A dictionary containing a success message if the transaction is added successfully.
        dict: An error message with a 404 status code if there are issues with the transaction data.
    """
    cur = conn.cursor()  # Initialize a cursor
    try:
        user_id = get_jwt_identity()["id"]  # Get user ID from JWT
        address = request.form.get("address")
        fullname = request.form.get("fullname")
        phone_number = request.form.get("phone_number")
        cart_ids = request.form.getlist("cart_ids")
        form = add_transaction_from_cart_form(request.form)
        if not form.validate():
            errors = {field.name: field.errors for field in form if field.errors}
            raise ValueError(errors)
        for cart_id in cart_ids:
            if not isinstance(cart_id, int):
                raise ValueError(f"Invalid cart ID: {cart_id} (must be an integer)")
            break
        # Begin a transaction
        transaction = add_transaction(user_id, address, fullname, phone_number)
        
        # Add transaction details from each cart
        for cart_id in cart_ids:
            cart = get_cart_by_cart_id_and_user_id(cart_id, user_id)
            
            # Check if the cart exists
            if cart is None:
                raise DatabaseError(f"Cart dengan ID {cart_id} tidak ditemukan")
            
            product = get_product_by_id(cart["product_id"])
            quantity = int(cart["quantity"])
            
            # Check if there is enough quantity of the product
            if int(product["quantity"]) < quantity:
                raise DatabaseError(
                    f"Stok dari produk dengan ID {product['id']} hanya tersisa {product['quantity']} barang"
                )
            
            # Calculate subtotal and add transaction details
            sub_total = product["price"] * quantity
            product_price = product["price"]
            add_transaction_details(
                transaction, product["id"], product_price, quantity, sub_total
            )
            
            # Update the quantity of the product and delete the cart
            updated_quantity = product["quantity"] - quantity
            update_product_quantity(product["id"], updated_quantity)
            delete_cart_by_id(cart_id)
        
        # Commit the transaction
        conn.commit()
        return {"message": "Berhasil ditambahkan"}, 200
    
    except DatabaseError as a:
        # Rollback transaction and return error message for database error
        conn.rollback()
        return {"error": str(a)}, 404
    except ValueError as v:
        # Rollback transaction and return error message for value error
        conn.rollback()
        return {"errors": v.args[0]}, 404
    except Exception as e:
        # Rollback transaction and raise exception for other errors
        conn.rollback()
        raise e
    finally:
        # Close the cursor
        cur.close()



def delete_user_transaction_controller():
    """
    Controller function to delete user transactions.

    Returns:
        dict: A dictionary containing a success message if the transactions are deleted successfully.
        dict: An error message with a 422 status code if there are issues with the deletion process.
    """
    try:
        user_id = get_jwt_identity()["id"]  # Get user ID from JWT
        delete_transaction_by_user_id(user_id)  # Delete transactions by user ID
        return {"message": "Berhasil dihapus"}, 200
    
    except Exception as e:
        # Rollback transaction and return error message for other errors
        conn.rollback()
        raise e



# TRANSACTION DETAILS


def get_transaction_details_by_transaction_id_controller(transaction_id: int):
    """
    Controller function to retrieve transaction details by transaction ID.

    Parameters:
        transaction_id (int): The ID of the transaction.

    Returns:
        dict: Transaction details if found.
        dict: An error message with a 404 status code if the transaction details are not found.
    """
    try:
        # Check if transaction exists with the given ID
        if get_transactions_by_id(transaction_id) is None:
            raise DatabaseError("Anda belum memiliki transaksi")
        
        data = get_transaction_details_by_transaction_id(transaction_id)
        # Check if transaction details exist
        if data is not None:
            return get_transaction_details_by_transaction_id(transaction_id)
        
        raise DatabaseError("Detail transaksi anda masih kosong")
    
    except DatabaseError as e:
        return {"error": str(e),"data": []}, 404
    except Exception as e:
        raise e

