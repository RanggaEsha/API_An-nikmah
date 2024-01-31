from db import conn

def get_all_carts(page: int, limit: int, max_date: int, min_date: int):
    """
    Retrieve all carts based on pagination and optional date range filters.

    Parameters:
        page (int): The page number for pagination.
        limit (int): The maximum number of carts per page.
        max_date (int): The maximum date (timestamp) for filtering carts.
        min_date (int): The minimum date (timestamp) for filtering carts.

    Returns:
        list or None: A list of dictionaries containing cart information if carts are found, otherwise None.
        Each dictionary contains the following keys:
        - "id" (int): Cart ID.
        - "user_id" (int): User ID associated with the cart.
        - "product_id" (int): Product ID in the cart.
        - "quantity" (int): Quantity of the product in the cart.
    """
    cur = conn.cursor()
    try:
        page = int(page)
        limit = int(limit)
        page = (page - 1) * limit
        values = {"limit": limit, "offset": page}
        where = []
        
        # Constructing the WHERE clause based on date filters
        if max_date and min_date:
            where.append("created_at BETWEEN %(min_date)s AND %(max_date)s")
            values["min_date"] = min_date
            values["max_date"] = max_date
        elif min_date:
            where.append("created_at >= %(min_date)s")
            values["min_date"] = min_date
        elif max_date:
            where.append("created_at <= %(max_date)s")
            values["max_date"] = max_date
        
        # Constructing the final WHERE clause
        if where:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ""
        
        # Constructing and executing the query
        query = f"""
        SELECT * FROM carts {where}
        LIMIT %(limit)s OFFSET %(offset)s
        """
        cur.execute(query, values)
        
        # Fetching and formatting the result
        list_data = []
        data = cur.fetchall()
        if not data and page >= cur.rowcount:
            return {"data": []}
        if data is not None:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "product_id": item[2],
                    "quantity": item[3],
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


def get_carts_by_user_id(user_id: int, page: int, limit: int, max_date: int, min_date: int):
    """
    Retrieve carts for a specific user based on pagination and optional date range filters.

    Parameters:
        user_id (int): The ID of the user whose carts are to be retrieved.
        page (int): The page number for pagination.
        limit (int): The maximum number of carts per page.
        max_date (int): The maximum date (timestamp) for filtering carts.
        min_date (int): The minimum date (timestamp) for filtering carts.

    Returns:
        list or None: A list of dictionaries containing cart information if carts are found, otherwise None.
        Each dictionary contains the following keys:
        - "id" (int): Cart ID.
        - "user_id" (int): User ID associated with the cart.
        - "product_id" (int): Product ID in the cart.
        - "quantity" (int): Quantity of the product in the cart.
    """
    cur = conn.cursor()
    try:
        page = int(page)
        limit = int(limit)
        page = (page - 1) * limit
        where = []
        values = {"limit": limit, "offset": page}
        
        # Constructing the WHERE clause based on user ID and date filters
        if user_id:
            where.append("user_id = %(user_id)s")
            values["user_id"] = user_id
        if max_date and min_date:
            where.append("created_at BETWEEN %(min_date)s AND %(max_date)s")
            values["min_date"] = min_date
            values["max_date"] = max_date
        elif min_date:
            where.append("created_at >= %(min_date)s")
            values["min_date"] = min_date
        elif max_date:
            where.append("created_at <= %(max_date)s")
            values["max_date"] = max_date
        
        # Constructing the final WHERE clause
        if where:
            where = "WHERE " + " AND ".join(where)

        # Constructing and executing the query
        query = f"""
        SELECT * FROM carts {where}
        LIMIT %(limit)s OFFSET %(offset)s
        """
        cur.execute(query, values)
        
        # Fetching and formatting the result
        list_data = []
        data = cur.fetchall()
        if not data and page >= cur.rowcount:
            return {"data": []}
        if data is not None:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "product_id": item[2],
                    "quantity": item[3],
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



def get_cart_by_cart_id_and_user_id(cart_id: int, user_id: int):
    """
    Retrieve a cart by its ID and associated user ID.

    Parameters:
        cart_id (int): The ID of the cart to retrieve.
        user_id (int): The ID of the user associated with the cart.

    Returns:
        dict or None: A dictionary containing cart information if the cart is found, otherwise None.
        The dictionary contains the following keys:
        - "id" (int): Cart ID.
        - "user_id" (int): User ID associated with the cart.
        - "product_id" (int): Product ID in the cart.
        - "quantity" (int): Quantity of the product in the cart.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, user_id, product_id, quantity FROM carts WHERE id = %s AND user_id = %s", (cart_id, user_id)
        )
        data = cur.fetchone()
        if data is not None:
            new_data = {
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
            }
            return new_data
        else:
            return None

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def get_carts_by_user_id_and_product_id(user_id: int, product_id: int):
    """
    Retrieve a cart by user ID and product ID.

    Parameters:
        user_id (int): The ID of the user associated with the cart.
        product_id (int): The ID of the product in the cart.

    Returns:
        dict or None: A dictionary containing cart information if the cart is found, otherwise None.
        The dictionary contains the following keys:
        - "id" (int): Cart ID.
        - "user_id" (int): User ID associated with the cart.
        - "product_id" (int): Product ID in the cart.
        - "quantity" (int): Quantity of the product in the cart.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, user_id, product_id, quantity FROM carts WHERE user_id = %s AND product_id = %s",
            (user_id, product_id),
        )
        conn.commit()
        data = cur.fetchone()
        if data is not None:
            new_data = {
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
            }
            return new_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def add_carts(user_id: int, product_id: int, quantity: int):
    """
    Add a new item to the user's cart.

    Parameters:
        user_id (int): The ID of the user adding the item to the cart.
        product_id (int): The ID of the product being added to the cart.
        quantity (int): The quantity of the product being added.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO carts (product_id, user_id, quantity) VALUES (%s, %s, %s)",
            (product_id, user_id, quantity),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def update_cart(product_id: int, user_id: int, quantity: int):
    """
    Update the quantity of a product in the user's cart.

    Parameters:
        product_id (int): The ID of the product in the cart to be updated.
        user_id (int): The ID of the user whose cart is being updated.
        quantity (int): The new quantity of the product in the cart.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE carts SET quantity=%s WHERE user_id=%s AND product_id=%s",
            (quantity, user_id, product_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_cart_by_user_id(user_id: int):
    """
    Delete all carts associated with a specific user.

    Parameters:
        user_id (int): The ID of the user whose carts are to be deleted.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM carts WHERE user_id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()



def delete_cart_by_user_id_and_cart_id(cart_id: int, user_id: int):
    """
    Delete a specific cart associated with a user.

    Parameters:
        cart_id (int): The ID of the cart to be deleted.
        user_id (int): The ID of the user whose cart is to be deleted.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        
        cur.execute(
            "DELETE FROM carts WHERE id = %s and user_id = %s",
            (cart_id,user_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()



def delete_cart_by_id(id: int):
    """
    Delete a cart by its ID.

    Parameters:
        id (int): The ID of the cart to be deleted.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM carts WHERE id = %s", (id,))
    except Exception as e:
        raise e
    finally:
        cur.close()

