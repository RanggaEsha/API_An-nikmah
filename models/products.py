from db import conn
from datetime import datetime


def get_all_products(
    page: int, limit: int, category: str, keyword: str, min_price: int, max_price: int, order_by:str,sort: str='asc'
):
    """
    Retrieve a list of products based on specified parameters.

    Parameters:
    - page (int): The page number for pagination.
    - limit (int): The number of products to retrieve per page.
    - category (str): The category name for filtering products (optional).
    - keyword (str): The keyword to search for in product names (optional).
    - min_price (int): The minimum price for filtering products (optional).
    - max_price (int): The maximum price for filtering products (optional).

    Returns:
    - list: A list of dictionaries representing products.
        data = [{
                    "id": item[0],
                    "name": item[1],
                    "description": item[2],
                    "price": item[3],
                    "quantity": item[4],
                    "created_at": item[5],
                    "category": item[8],
                    "category_id": item[6],
                }]
    Each dictionary contains the following keys:
        - "id" (int): Product ID.
        - "name" (str): Product name.
        - "description" (str): Product description.
        - "price" (float): Product price.
        - "quantity" (int): Product quantity.
        - "created_at" (str): Product creation timestamp.
        - "category" (str, optional): Product category name (present only if category is specified).
        - "category_id" (int): Product category ID.
    """
    cur = conn.cursor()
    try:
        page = int(page)
        page = (page - 1) * limit
        values = {"limit": limit, "offset": page}
        join = []
        where = []
        whitelist_orders = [
        "id", "name","price","category_id"
        ]
        if order_by:
            if order_by not in whitelist_orders:
                raise ValueError("Value Order By tidak ada didalam whitelist, whitelist yang tersedia: "+", ".join(whitelist_orders))
        else:
            order_by = ''
        whitelist_sorts=[
            "asc","desc"
        ]
        if sort:
            if sort not in whitelist_sorts:
                raise ValueError("Value Sort By tidak ada didalam whitelist, whitelist yang tersedia: "+", ".join(whitelist_sorts))
        else:
            sort = ''
        if keyword:
            where.append("p.name ilike %(keyword)s")
            values["keyword"] = "%" + keyword + "%"
        if category:
            where.append("categories.name ilike %(category)s")
            join.append("JOIN categories on p.category_id = categories.id")
            values["category"] = "%" + category + "%"
        if max_price and min_price:
            where.append("price BETWEEN %(min_price)s AND %(max_price)s")
            values["min_price"] = min_price
            values["max_price"] = max_price
        elif min_price:
            where.append("price >= %(min_price)s")
            values["min_price"] = min_price
        elif max_price:
            where.append("price <= %(max_price)s")
            values["max_price"] = max_price
        
        if len(where) > 0:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ""

        if not order_by and sort:
            raise ValueError("harus menginputkan juga order_by, wihtelist yang tersedia: "+", ".join(whitelist_orders))
        if order_by:
            order = f"ORDER BY {order_by}"
            if sort:
                sort
            else:
                sort = ''
        else:
            order =''
        query = f"""
        SELECT * FROM products p 
        {' '.join(join)} {where}
        {order} {sort}
        limit %(limit)s offset %(offset)s
        """
        print(query,values)
        cur.execute(query, values)
        
        conn.commit()
        products = cur.fetchall()
        if not products and page >= cur.rowcount:
            return {"data": []}
        list_products = []
        for item in products:
            if category is not None:
                items = {
                    "id": item[0],
                    "name": item[1],
                    "description": item[2],
                    "price": item[3],
                    "quantity": item[4],
                    "created_at": item[5],
                    "category": item[8],
                    "category_id": item[6],
                }
                list_products.append(items)
            else:
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
        print(query, values)
        return list_products
    except ValueError as e:
        return {"message": str(e)}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_products_by_category(category_id: int):
    """
    Retrieve a list of products based on a specified category ID.

    Parameters:
    - category_id (int): The ID of the category for which products are to be retrieved.

    Returns:
     - list: A list of dictionaries representing products.
        data = [{
                    "id": item[0],
                    "name": item[1],
                    "description": item[2],
                    "price": item[3],
                    "quantity": item[4],
                    "created_at": item[5],
                    "category": item[8],
                    "category_id": item[6],
                }]
      Each dictionary contains the following keys:
        - "id" (int): Product ID.
        - "name" (str): Product name.
        - "description" (str): Product description.
        - "price" (float): Product price.
        - "quantity" (int): Product quantity.
        - "created_at" (str): Product creation timestamp.
        - "category_id" (int): Product category ID.
    If no products are found, returns None.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, name, description, price, quantity, created_at, category_id
            FROM products
            where category_id=%(category_id)s
            order by id asc 
        """,
            {"category_id": category_id},
        )
        result_set = cur.fetchall()
        if result_set:
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
        else:
            return None
    except Exception as e:
        raise e
    finally:
        cur.close()


def get_product_by_id(id: int):
    """
    Retrieve a product based on a specified product ID.

    Parameters:
    - id (int): The ID of the product to be retrieved.

    Returns:
    - dict or None: A dictionary representing the product with the specified ID.
     - list: A list of dictionaries representing products.
        data = {
                    "id": data[0],
                    "name": data[1],
                    "description": data[2],
                    "price": data[3],
                    "quantity": data[4],
                    "created_at": data[5],
                    "category": data[8],
                    "category_id": data[6],
                }
      The dictionary contains the following keys:
        - "id" (int): Product ID.
        - "name" (str): Product name.
        - "description" (str): Product description.
        - "price" (float): Product price.
        - "quantity" (int): Product quantity.
        - "created_at" (str): Product creation timestamp.
        - "category_id" (int): Product category ID.
    If no product is found with the specified ID, returns None.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id,name,description,price,quantity,created_at,category_id
            FROM products
            where id = %s      
            order by id asc 
        """,
            (id,),
        )
        row = cur.fetchone()
        if row is not None:
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
        else:
            return None
    except Exception as e:
        raise e
    finally:
        cur.close()


def upload_product(name, description, price, quantity, category_id):
    """
    Upload a new product to the database.

    Parameters:
    - name (str): The name of the product.
    - description (str): The description of the product.
    - price (float): The price of the product.
    - quantity (int): The quantity of the product.
    - category_id (int): The ID of the category to which the product belongs.

    Returns:
    - int: The ID of the newly uploaded product.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO products (name, description, price, quantity, created_at, category_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """,
            (name, description, price, quantity, "now()", category_id),
        )
        conn.commit()
        return cur.fetchone()[0]

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()


def update_product(product_id, name, description, price, quantity, category_id):
    """
    Update an existing product in the database.

    Parameters:
    - product_id (int): The ID of the product to be updated.
    - name (str): The updated name of the product.
    - description (str): The updated description of the product.
    - price (float): The updated price of the product.
    - quantity (int): The updated quantity of the product.
    - category_id (int): The updated ID of the category to which the product belongs.

    Returns:
    - None
    """
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
        return "File updated successfully"
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()

    


def update_product_quantity(product_id, quantity):
    """
    Update the quantity of an existing product in the database.

    Parameters:
    - product_id (int): The ID of the product whose quantity is to be updated.
    - quantity (int): The updated quantity of the product.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE products 
            SET quantity=%s
            WHERE id=%s
        """,
            (
                quantity,
                product_id,
            ),
        )

    except Exception as e:
        raise e

    finally:
        cur.close()


def delete_product(product_id):
    """
    Delete a product from the database based on its ID.

    Parameters:
    - product_id (int): The ID of the product to be deleted.

    Returns:
    - None
    """
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


def get_all_product_images(product_id):
    """
    Retrieve a list of images associated with a specific product.

    Parameters:
    - product_id (int): The ID of the product for which images are to be retrieved.

    Returns:
    - list or None: A list of dictionaries representing product images.
      Each dictionary contains the following keys:
        - "id" (int): Image ID.
        - "image" (str): Image URL or file path.
    If no images are found for the specified product, returns None.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id,image FROM product_images where product_id = %s", (product_id,)
        )
        images = cur.fetchall()

        list_images = []
        if images:
            for image in images:
                item = {"id": image[0], "image": image[1]}
                list_images.append(item)
            return list_images
        else:
            return None

    except Exception as e:
        raise e
    finally:
        cur.close()


def get_image_by_product_id_and_image_id(id,product_id):
    """
    Retrieve a product image based on its ID.

    Parameters:
    - id (int): The ID of the product image to be retrieved.

    Returns:
    - dict: A dictionary representing the product image with the specified ID.
      The dictionary contains the following keys:
        - "id" (int): Image ID.
        - "image" (str): Image URL or file path.
        - "product_id" (int): ID of the product to which the image belongs.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM product_images where id = %s AND product_id = %s", (id,product_id))
        image = cur.fetchone()
        if image:
            new_image = {"id": image[0], "image": image[1], "product_id": image[2]}
            return new_image
        else:
            return None
    except Exception as e:
        raise e
    finally:
        cur.close()


def upload_product_images(image_location, product_id):
    """
    Upload product images to the database for a specific product.

    Parameters:
    - image_location (list): List of image URLs or file paths.
    - product_id (int): The ID of the product to which the images belong.

    Returns:
    - None
    """
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


def delete_image_by_id(product_id,image_id):
    """
    Delete a product image from the database based on its ID.

    Parameters:
    - id (int): The ID of the product image to be deleted.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE from product_images where id = %s AND product_id = %s", (image_id,product_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_images_by_product_id(product_id):
    """
    Delete all product images associated with a specific product.

    Parameters:
    - product_id (int): The ID of the product for which images are to be deleted.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE from product_images where product_id = %s", (product_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
