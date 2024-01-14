from db import conn
from datetime import datetime

def get_all_products():
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.id, p.name, p.description, p.price, p.quantity, p.created_at, p.category_id,
                   pi.id AS image_id, pi.image AS image_url
            FROM products p
            LEFT JOIN product_images pi ON p.id = pi.product_id
        """)
        result_set = cur.fetchall()
        # return result_set

        products = {}
        for row in result_set:
            product_id = row[0]
            if product_id not in products:
                products[product_id] = {
                    "id": product_id,
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "quantity": row[4],
                    "created_at": row[5],
                    "category_id": row[6],
                    "images": [],
                }

            if row[7] is not None:
                products[product_id]["images"].append({"id": row[7], "image": row[8]})

        return list(products.values())
    except Exception as e:
        raise e
    finally:
        cur.close()


# def get_all_products():
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT * FROM products")
#         products = cur.fetchall()

#         list_products = []
#         for item in products:
#             items = {
#                 "id": item[0],
#                 "name": item[1],
#                 "description": item[2],
#                 "price": item[3],
#                 "quantity": item[4],
#                 "created_at": item[5],
#                 "category_id": item[6],
#                 "images": [],
#             }
#             list_products.append(items)

#             # get images
#             cur.execute(
#                 "SELECT * FROM product_images WHERE product_id = %s", (item[0],)
#             )
#             images = cur.fetchall()

#             for image in images:
#                 item_image = {"id": image[0], "image": image[1]}

#                 list_products[-1]["images"].append(item_image)

#         return list_products
#     except Exception as e:
#         raise e
#     finally:
#         cur.close()


def get_products_by_category(category_id):

    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.id, p.name, p.description, p.price, p.quantity, p.created_at, p.category_id,
                   pi.id AS image_id, pi.image AS image_url
            FROM products p
            LEFT JOIN product_images pi ON p.id = pi.product_id
            where p.category_id=%s
            order by p.id asc 
        """,(category_id,))

        result_set = cur.fetchall()

        products = {}
        for row in result_set:
            product_id = row[0]
            if product_id not in products:
                products[product_id] = {
                    "id": product_id,
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "quantity": row[4],
                    "created_at": row[5],
                    "category_id": row[6],
                    "images": [],
                }

            if row[7] is not None:
                products[product_id]["images"].append({"id": row[7], "image": row[8]})

        return list(products.values())
    except Exception as e:
        raise e
    finally:
        cur.close()


def get_products_by_id(id):

    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.id, p.name, p.description, p.price, p.quantity, p.created_at, p.category_id,
                   pi.id AS image_id, pi.image AS image_url
            FROM products p
            LEFT JOIN product_images pi ON p.id = pi.product_id
            where p.id=%s
            order by p.id asc 
        """,(id,))

        result_set = cur.fetchall()
        # return result_set

        products = {}
        for row in result_set:
            product_id = row[0]
            if product_id not in products:
                products[product_id] = {
                    "id": product_id,
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "quantity": row[4],
                    "created_at": row[5],
                    "category_id": row[6],
                    "images": [],
                }

            if row[7] is not None:
                products[product_id]["images"].append({"id": row[7], "image": row[8]})

        return list(products.values())
    except Exception as e:
        raise e
    finally:
        cur.close()


def get_products_by_price_range(max_price, min_price):
    cur = conn.cursor()
    try:
        if max_price and min_price:
            cur.execute("""
                SELECT p.id, p.name, p.description, p.price, p.quantity, p.created_at, p.category_id,
                    pi.id AS image_id, pi.image AS image_url
                FROM products p
                LEFT JOIN product_images pi ON p.id = pi.product_id
                WHERE p.price > %s AND p.price < %s;
            """, (min_price, max_price))
        elif not min_price:
            cur.execute("""
                SELECT p.id, p.name, p.description, p.price, p.quantity, p.created_at, p.category_id,
                    pi.id AS image_id, pi.image AS image_url
                FROM products p
                LEFT JOIN product_images pi ON p.id = pi.product_id
                WHERE p.price < %s;
            """, (max_price,))
        elif not max_price:
            cur.execute("""
                SELECT p.id, p.name, p.description, p.price, p.quantity, p.created_at, p.category_id,
                    pi.id AS image_id, pi.image AS image_url
                FROM products p
                LEFT JOIN product_images pi ON p.id = pi.product_id
                WHERE p.price > %s;
            """, (min_price,))
        
        result_set = cur.fetchall()
        products = {}
        for row in result_set:
            product_id = row[0]
            if product_id not in products:
                products[product_id] = {
                    "id": product_id,
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "quantity": row[4],
                    "created_at": row[5],
                    "category_id": row[6],
                    "images": [],
                }

            if row[7] is not None:
                products[product_id]["images"].append({"id": row[7], "image": row[8]})

        return list(products.values())
    except Exception as e:
        raise e
    finally:
        cur.close()



def upload_product(name, description, price, quantity, category_id, image_location):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO products (name, description, price, quantity, created_at, category_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """,
            (name, description, price, quantity, datetime.now(), category_id),
        )
        last_inserted_id = cur.fetchone()[0]

        for image in image_location:
            cur.execute(
                "INSERT INTO product_images (image, product_id) VALUES (%s, %s)",
                (image, last_inserted_id),
            )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    return "File uploaded successfully"


def update_product(
    product_id, name, description, price, quantity, category_id, image_location
):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE products 
            SET name=%s, description=%s, price=%s, quantity=%s, created_at=%s, category_id=%s
            WHERE id=%s
        """,
            (
                name,
                description,
                price,
                quantity,
                datetime.now(),
                category_id,
                product_id,
            ),
        )
        # last_inserted_id = cur.fetchone()[0]

        if image_location:
            cur.execute(
                "DELETE FROM product_images WHERE product_id=%s", (image_location,)
            )

            for image in image_location:
                cur.execute(
                    "INSERT INTO product_images (image, product_id) VALUES (%s, %s)",
                    (image, product_id),
                )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    return "File updated successfully"


def delete_product(product_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        cur.execute("DELETE FROM product_images WHERE product_id = %s", (product_id,))
        # data = cur.fetchone()
        # return(data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
