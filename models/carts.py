from db import conn

def get_carts_by_user_id(user_id):
    cur = conn.cursor()
    try:
        cur.execute('SELECT id,user_id,product_id,quantity FROM carts WHERE user_id = %s', (user_id,))
        data = cur.fetchone()
    
        if data is not None:
            new_data = {
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3]
            }
            return new_data
        else:
            return None
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def get_carts_by_user_id_and_product_id(user_id,product_id):
    cur = conn.cursor()
    try:
        cur.execute('SELECT id,user_id,product_id,quantity FROM carts WHERE user_id = %s AND product_id=%s', (user_id,product_id))
        conn.commit()
        data = cur.fetchone()
        if data is not None:
            new_data = {
                "id": data[0],
                "user_id": data[1],
                "product_id": data[2],
                "quantity": data[3]
            }
            return new_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def add_carts(user_id,product_id,quantity):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO carts (product_id,user_id,quantity) VALUES (%s,%s,%s)",(product_id,user_id,quantity))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def update_cart(user_id,product_id,quantity):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE carts SET product_id=%s,quantity=%s where user_id=%s",(product_id,quantity,user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_cart_by_user_id(user_id):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM carts WHERE user_id = %s', (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()