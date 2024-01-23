from db import conn


def get_carts_by_user_id(user_id: int):
    """
    Retrieve carts based on user ID.

    Parameters:
    - user_id (int): The ID of the user whose carts are to be retrieved.

    Returns:
    - List:
        data = [{
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
            }]
    - None: A list containing dictionaries with cart information including cart ID, user ID, product ID, and quantity, or None if no carts are found for the user.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id,user_id,product_id,quantity FROM carts WHERE user_id = %s",
            (user_id,),
        )
        data = cur.fetchall()
        list_data = []
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


def get_cart_by_id(id: int):
    """
    Retrieve carts based on cart ID.

    Parameters:
    - id (int): The ID of the user whose carts are to be retrieved.

    Returns:
    - Dict:
        data = {
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
            }
    - None: A dict containing cart information including cart ID, user ID, product ID, and quantity, or None if no carts are found for the user.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id,user_id,product_id,quantity FROM carts WHERE id = %s", (id,)
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
    Retrieve a specific cart based on user ID and product ID.

    Parameters:
    - user_id (int): The ID of the user.
    - product_id (int): The ID of the product.

    Returns:
    - Dict:
        data = {
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
            }
    - None: A dictionary containing cart information including cart ID, user ID, product ID, and quantity, or None if the specified cart is not found.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id,user_id,product_id,quantity FROM carts WHERE user_id = %s AND product_id=%s",
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
    Add a new cart entry.

    Parameters:
    - user_id (int): The ID of the user.
    - product_id (int): The ID of the product.
    - quantity (int): The quantity of the product in the cart.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO carts (product_id,user_id,quantity) VALUES (%s,%s,%s)",
            (product_id, user_id, quantity),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def update_cart(product_id, user_id, quantity):
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE carts SET quantity=%s where user_id=%s and product_id=%s",
            (quantity, user_id, product_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_cart_by_user_id(user_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM carts WHERE user_id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_cart_by_user_id_and_product_id(user_id, product_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM carts WHERE user_id = %s and product_id = %s",
            (user_id, product_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_cart_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM carts WHERE id = %s", (id,))
    except Exception as e:
        raise e
    finally:
        cur.close()
