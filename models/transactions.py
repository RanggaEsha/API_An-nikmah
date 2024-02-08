from db import conn
from datetime import datetime

def get_all_transactions(limit: int, page: int, max_date: int, min_date: int):
    """
    Retrieve a list of transactions based on provided filters.

    Parameters:
        limit (int): The maximum number of transactions per page.
        page (int): The page number for pagination.
        max_date (int): The maximum date for filtering transactions.
        min_date (int): The minimum date for filtering transactions.

    Returns:
        list: A list of dictionaries containing transaction information.
        Each dictionary contains the following keys:
        - "id" (int): Transaction ID.
        - "user_id" (int): ID of the user associated with the transaction.
        - "address" (str): Address associated with the transaction.
        - "fullname" (str): Full name associated with the transaction.
        - "phone_number" (str): Phone number associated with the transaction.
        - "created_at" (str): Timestamp indicating when the transaction was created.
    """
    cur = conn.cursor()
    try:
        page = int(page)
        limit = int(limit)
        page = (page - 1) * limit
        where = []
        values = {"limit": limit, "offset": page}
        
        # Check if both max_date and min_date are provided
        if max_date and min_date:
            where.append("created_at BETWEEN %(min_date)s AND %(max_date)s")
            values["min_date"] = min_date
            values["max_date"] = max_date
        elif min_date:
            # Add filter for minimum date
            where.append("created_at >= %(min_date)s")
            values["min_date"] = min_date
        elif max_date:
            # Add filter for maximum date
            where.append("created_at <= %(max_date)s")
            values["max_date"] = max_date
            
        # Construct WHERE clause based on provided filters
        if len(where) > 0:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ''

        # Construct SQL query for retrieving transactions
        query = (f"""
        SELECT * FROM transactions p {where}
        limit %(limit)s offset %(offset)s
        """)
        
        # Execute SQL query
        cur.execute(query, values)
        
        list_data = []
        data = cur.fetchall()
        
        # If no transactions are fetched and the page exceeds the total number of rows, return an empty data list 
        if not data and page >= cur.rowcount:
            return {"data": []}
        
        # Prepare fetched transactions for response
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "address": item[2],
                    "fullname": item[3],
                    "phone_number": item[4],
                    "created_at": item[5],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_transactions_by_id(id):
    """
    Retrieve a transaction by its ID.

    Parameters:
        id (int): The ID of the transaction to be retrieved.

    Returns:
        list or None: A list of dictionaries containing transaction information if the transaction is found,
        otherwise None.
        Each dictionary contains the following keys:
        - "id" (int): Transaction ID.
        - "user_id" (int): ID of the user associated with the transaction.
        - "address" (str): Address associated with the transaction.
        - "fullname" (str): Full name associated with the transaction.
        - "phone_number" (str): Phone number associated with the transaction.
        - "created_at" (str): Timestamp indicating when the transaction was created.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM transactions WHERE id = %s", (id,))
        data = cur.fetchall()
        list_data = []
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "address": item[2],
                    "fullname": item[3],
                    "phone_number": item[4],
                    "created_at": item[5],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_transactions_by_user_id(user_id: int, limit: int, page: int, max_date: int, min_date: int):
    """
    Retrieve a list of transactions for a specific user based on provided filters.

    Parameters:
        user_id (int): The ID of the user for whom transactions are to be retrieved.
        limit (int): The maximum number of transactions per page.
        page (int): The page number for pagination.
        max_date (int): The maximum date for filtering transactions.
        min_date (int): The minimum date for filtering transactions.

    Returns:
        list: A list of dictionaries containing transaction information.
        Each dictionary contains the following keys:
        - "id" (int): Transaction ID.
        - "user_id" (int): ID of the user associated with the transaction.
        - "address" (str): Address associated with the transaction.
        - "fullname" (str): Full name associated with the transaction.
        - "phone_number" (str): Phone number associated with the transaction.
        - "created_at" (str): Timestamp indicating when the transaction was created.
    """
    cur = conn.cursor()
    try:
        page = int(page)
        limit = int(limit)
        page = (page - 1) * limit
        where = []
        values = {"limit": limit, "offset": page}
        
        # Check if both max_date and min_date are provided
        if max_date and min_date:
            where.append("created_at BETWEEN %(min_date)s AND %(max_date)s")
            values["min_date"] = min_date
            values["max_date"] = max_date
        elif min_date:
            # Add filter for minimum date
            where.append("created_at >= %(min_date)s")
            values["min_date"] = min_date
        elif max_date:
            # Add filter for maximum date
            where.append("created_at <= %(max_date)s")
            values["max_date"] = max_date
            
        # Add filter for user ID
        if user_id:
            where.append("user_id = %(user_id)s")
            values["user_id"] = user_id
            
        # Construct WHERE clause based on provided filters
        if len(where) > 0:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ""

        # Construct SQL query for retrieving transactions
        query = (f"""
        SELECT * FROM transactions p {where}
        limit %(limit)s offset %(offset)s
        """)
        
        # Execute SQL query
        cur.execute(query, values)
        
        list_data = []
        data = cur.fetchall()
        
        # If no transactions are fetched and the page exceeds the total number of rows, return an empty data list 
        if not data and page >= cur.rowcount:
            return {"data": []}
        
        # Prepare fetched transactions for response
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "address": item[2],
                    "fullname": item[3],
                    "phone_number": item[4],
                    "created_at": item[5],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()



def add_transaction(user_id: int, address: str, fullname: str, phone_number: int):
    """
    Add a new transaction to the database.

    Parameters:
        user_id (int): The ID of the user associated with the transaction.
        address (str): The address associated with the transaction.
        fullname (str): The full name associated with the transaction.
        phone_number (str): The phone number associated with the transaction.

    Returns:
        int: The ID of the newly added transaction.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO transactions (user_id, address, fullname, phone_number, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (user_id, address, fullname, phone_number, 'now()'),
        )
        return cur.fetchone()[0]
    except Exception as e:
        raise e
    finally:
        cur.close()


def delete_transaction_by_user_id(user_id: int):
    """
    Delete transactions associated with a specific user from the database.

    Parameters:
        user_id (int): The ID of the user whose transactions are to be deleted.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE from transactions where user_id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()



def delete_transaction_by_id(id: int):
    """
    Delete a transaction from the database based on its ID.

    Parameters:
        id (int): The ID of the transaction to be deleted.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE from transactions where id = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


# TRANSACTION DETAILS


def get_transaction_details_by_transaction_id(transaction_id: int):
    """
    Retrieve transaction details associated with a specific transaction ID.

    Parameters:
        transaction_id (int): The ID of the transaction to retrieve details for.

    Returns:
        list or None: A list containing dictionaries with transaction detail information,
        including detail ID, transaction ID, product ID, product price, quantity, sub total, and creation timestamp.
        Returns None if no details are found for the specified transaction ID.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM transaction_details WHERE transaction_id = %s",
            (transaction_id,),
        )
        data = cur.fetchall()
        list_data = []
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "transaction_id": item[1],
                    "product_id": item[2],
                    "product_price": item[3],
                    "quantity": item[4],
                    "sub_total": item[5],
                    "created_at": item[6],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_transaction_details_by_user_id_and_product_id(user_id: int, product_id: int):
    """
    Retrieve transaction details associated with a specific user ID and product ID.

    Parameters:
        user_id (int): The ID of the user.
        product_id (int): The ID of the product.

    Returns:
        dict or None: A dictionary containing transaction detail information if found,
        including detail ID, transaction ID, product ID, quantity, price, and creation timestamp.
        Returns None if no details are found for the specified user ID and product ID.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM transaction_details WHERE user_id = %s AND product_id = %s",
            (user_id, product_id),
        )
        data = cur.fetchone()
        if data is not None:
            new_data = {
                "id": data[0],
                "transaction_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
                "price": data[4],
                "created_at": data[5],
            }
            return new_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def add_transaction_details(transaction_id: int, product_id: int, product_price: int, quantity: int, sub_total: int):
    """
    Add transaction details to the database.

    Parameters:
        transaction_id (int): The ID of the transaction associated with the details.
        product_id (int): The ID of the product.
        product_price (float): The price of the product.
        quantity (int): The quantity of the product.
        sub_total (float): The subtotal of the transaction detail.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO transaction_details (transaction_id,product_id,product_price,quantity,sub_total) VALUES (%s,%s,%s,%s,%s)",
            (transaction_id, product_id, product_price, quantity, sub_total),
        )
    except Exception as e:
        raise e
    finally:
        cur.close()

