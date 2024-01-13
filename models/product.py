from db import conn  
import time
from datetime import datetime

def upload_product(name, description, price, quantity, category_id, image_location):
    
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO products (name, description, price, quantity, created_at, category_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (name, description, price, quantity,datetime.now(), category_id))
        last_inserted_id = cur.fetchone()[0]

        for image in image_location:
            cur.execute("INSERT INTO product_images (image, product_id) VALUES (%s, %s)", (image, last_inserted_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    return "File uploaded successfully"

def update_product(product_id, name, description, price, quantity, category_id, image_location):
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE products 
            SET name=%s, description=%s, price=%s, quantity=%s, created_at=%s, category_id=%s
            WHERE id=%s
        """, (name, description, price, quantity,datetime.now(), category_id, product_id))
        # last_inserted_id = cur.fetchone()[0]

        if image_location:
            cur.execute("DELETE FROM product_images WHERE product_id=%s", (image_location,))

            for image in image_location:
                cur.execute("INSERT INTO product_images (image, product_id) VALUES (%s, %s)", (image, product_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    return "File updated successfully"

def product_id_validator(product_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products where id=%s",(product_id,))
        if cur.fetchone():
           return True
    except Exception as e:
        raise e
    finally:
        cur.close()


def delete_product(product_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products WHERE id = %s",(product_id,))
        cur.execute("DELETE FROM product_images WHERE product_id = %s",(product_id,))
        # data = cur.fetchone()
        # return(data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

        
