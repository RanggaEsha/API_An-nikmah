from db import conn  #Pastikan untuk mengimpor objek koneksi 'conn' dari modul db
import time
from datetime import datetime

def upload_product(name, description, price, quantity, category_id, image_location):
    
    cur = conn.cursor()
    try:
        # Insert product information into the 'products' table
        cur.execute("""
            INSERT INTO products (name, description, price, quantity, created_at, category_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (name, description, price, quantity,datetime.now(), category_id))
        last_inserted_id = cur.fetchone()[0]

        # Insert image information into the 'product_images' table
        for image in image_location:
            cur.execute("INSERT INTO product_images (image, product_id) VALUES (%s, %s)", (image, last_inserted_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    return "File uploaded successfully"

def update_product(name, description, price, quantity,created_at, category_id, image_location):
    cur = conn.cursor()
    try:
        # Insert product information into the 'products' table
        cur.execute("""
            INSERT INTO products (name, description, price, quantity, created_at, category_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (name, description, price, quantity, created_at, category_id))
        last_inserted_id = cur.fetchone()[0]

        # Insert image information into the 'product_images' table
        cur.execute("INSERT INTO product_images (image, product_id) VALUES (%s, %s)", (image_location, last_inserted_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    return "File uploaded successfully"

