from db import conn
from datetime import datetime


def get_all_products(page: int, limit: int, keyword: str = None):
    cur = conn.cursor()
    try:
        page = int(page)
        page = (page - 1) * limit
        values = {"limit": limit, "offset": page}
        where_keyword = ""
        if keyword is not None:
            where_keyword = "WHERE name ilike %(keyword)s"
            values["keyword"] = "%" + keyword + "%"
        query = f"""SELECT * FROM products  {where_keyword} limit %(limit)s offset %(offset)s"""
        cur.execute(query, values)
        products = cur.fetchall()
        list_products = []
        for item in products:
            items = {
                "id": item[0],
                "name": item[1],
                "description": item[2],
                "price": item[3],
                "quantity": item[4],
                "created_at": item[5],
                "category_id": item[6],
            }
            list_products.append(items)

        return list_products
    except Exception as e:
        raise e
    finally:
        cur.close()


def get_products_by_category(category_id):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, name, description, price, quantity, created_at, category_id
            FROM products
            where category_id=%s
            order by id asc 
        """,
            (category_id,),
        )
        result_set = cur.fetchall()
        products = []
        for row in result_set:
            new_products = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "quantity": row[4],
                "created_at": row[5],
                "category_id": row[6],
            }
            products.append(new_products)
        return products
    except Exception as e:
        raise e
    finally:
        cur.close()


def get_products_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id,name,description,price,quantity,created_at,category_id
            FROM products
            where id=%s
            order by id asc 
        """,
            (id,),
        )
        row = cur.fetchone()
        new_product = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "quantity": row[4],
            "created_at": row[5],
            "category_id": row[6],
        }
        return new_product
    except Exception as e:
        raise e
    finally:
        cur.close()


def get_products_by_price_range(max_price, min_price):
    cur = conn.cursor()
    try:
        where_condition = ""
        values = None
        if max_price is not None and min_price is not None:
            where_condition = "price BETWEEN %(min_price)s AND %(max_price)s"
            values = {'min_price': min_price, 'max_price': max_price}          
        elif max_price is None:
            where_condition = "price >= %(min_price)s"
            values = {'min_price': min_price}
        elif min_price is None:
            where_condition = "price <= %(max_price)s"
            values = {'max_price': max_price}

        query = f"""
                SELECT id, name, description, price, quantity, created_at, category_id
                FROM products
                WHERE {where_condition}
                order by price asc;
            """
        print(query, values)
        cur.execute(query, values)

        result_set = cur.fetchall()
        products = []
        for row in result_set:
            new_product = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "quantity": row[4],
                "created_at": row[5],
                "category_id": row[6],
            }
            products.append(new_product)
        return products
    except Exception as e:
        raise e
    finally:
        cur.close()


def upload_product(name, description, price, quantity, category_id):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO products (name, description, price, quantity, created_at, category_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """,
            (name, description, price, quantity, datetime.now(), category_id),
        )
        conn.commit()
        return cur.fetchone()[0]

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()


def update_product(product_id, name, description, price, quantity, category_id):
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
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


# PRODUCT IMAGES MODELS


def all_product_images(product_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT image FROM product_images where product_id = %s", (product_id,)
        )
        images = cur.fetchall()

        list_images = []
        for image in images:
            item = {"image": image[0]}
            list_images.append(item)
        return list_images

    except Exception as e:
        raise e
    finally:
        cur.close()


def get_product_image_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM product_images where id = %s", (id,))
        image = cur.fetchone()
        new_image = {
            "id":image[0],
            "image":image[1],
            "product_id":image[2]
        }
        return new_image

    except Exception as e:
        raise e
    finally:
        cur.close()


def upload_product_images(image_location, product_id):
    cur = conn.cursor()
    try:
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


def delete_image_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE from product_images where id = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_images_by_product_id(product_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE from product_images where product_id = %s", (product_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
