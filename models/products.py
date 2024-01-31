from db import conn
from datetime import datetime

def get_all_products(
    page: int, limit: int, category: str, keyword: str, min_price: int, max_price: int, order_by: str, sort: str = 'asc'
):
    """
    Retrieve a list of products based on provided filters.

    Parameters:
        page (int): The page number for pagination.
        limit (int): The maximum number of products per page.
        category (str): The category of the products.
        keyword (str): The keyword to search for in product names.
        min_price (int): The minimum price of products to include.
        max_price (int): The maximum price of products to include.
        order_by (str): The field to order the products by.
        sort (str, optional): The sorting order ('asc' or 'desc'). Defaults to 'asc'.

    Returns:
        list: A list of dictionaries containing product information.
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
            "id", "name", "price", "category_id"
        ]
        # Check if the provided order_by field is valid
        if order_by:
            if order_by not in whitelist_orders:
                raise ValueError("Value Order By tidak ada didalam whitelist, whitelist yang tersedia: " + ", ".join(whitelist_orders))
        else:
            order_by = ''
        whitelist_sorts = [
            "asc", "desc"
        ]
        # Check if the provided sort field is valid
        if sort:
            if sort not in whitelist_sorts:
                raise ValueError("Value Sort By tidak ada didalam whitelist, whitelist yang tersedia: " + ", ".join(whitelist_sorts))
        else:
            sort = ''
        if keyword:
            # Add filter for product name based on keyword
            where.append("p.name ilike %(keyword)s")
            values["keyword"] = "%" + keyword + "%"
        if category:
            # Add filter for category name based on category
            where.append("categories.name ilike %(category)s")
            join.append("JOIN categories on p.category_id = categories.id")
            values["category"] = "%" + category + "%"
        if max_price and min_price:
            # Add filter for price range between min_price and max_price
            where.append("price BETWEEN %(min_price)s AND %(max_price)s")
            values["min_price"] = min_price
            values["max_price"] = max_price
        elif min_price:
            # Add filter for minimum price
            where.append("price >= %(min_price)s")
            values["min_price"] = min_price
        elif max_price:
            # Add filter for maximum price
            where.append("price <= %(max_price)s")
            values["max_price"] = max_price

        if len(where) > 0:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ""

        # Check if both order_by and sort are provided together
        if not order_by and sort:
            raise ValueError("harus menginputkan juga order_by, wihtelist yang tersedia: " + ", ".join(whitelist_orders))
        if order_by:
            order = f"ORDER BY {order_by}"
            # Ensure the sort parameter is included if provided
            if sort:
                sort
            else:
                sort = ''  # Assigning an empty string to sort if it's not provided
        else:
            order = ''
        query = f"""
        SELECT * FROM products p 
        {' '.join(join)} {where}
        {order} {sort}
        limit %(limit)s offset %(offset)s
        """

        cur.execute(query, values)

        conn.commit()
        products = cur.fetchall()
        # If no products are fetched and the page exceeds the total number of rows, return an empty data list 
        if not products and page >= cur.rowcount:
            return {"data": []}
        list_products = []
        # Iterate through fetched products and prepare them for response
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
    Retrieve products based on the provided category ID.

    Parameter:
        category_id (int): The ID of the category to retrieve products for.

    Returns:
        list or None: A list of dictionaries containing product information if found, otherwise None.
        Each dictionary contains the following keys:
        - "id" (int): Product ID.
        - "name" (str): Product name.
        - "description" (str): Product description.
        - "price" (float): Product price.
        - "quantity" (int): Product quantity.
        - "created_at" (str): Product creation timestamp.
        - "category_id" (int): Product category ID.
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


def upload_product(name: str, description: str, price: int, quantity: int, category_id: int):
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


def update_product(product_id: int, name: str, description: str, price: int, quantity: int, category_id: int):
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


def update_product_quantity(product_id: int, quantity: int):
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


def delete_product(product_id: int):
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


def get_all_product_images(product_id: int):
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


def get_image_by_product_id_and_image_id(image_id: int,product_id: int):
    """
    Retrieve a product image based on its ID.

    Parameters:
    - id (int): The ID of the product image to be retrieved.
    - product_id (int): The ID of the product the image belongs to.
    Returns:
    - dict: A dictionary representing the product image with the specified ID.
      The dictionary contains the following keys:
        - "id" (int): Image ID.
        - "image" (str): Image URL or file path.
        - "product_id" (int): ID of the product to which the image belongs.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM product_images where id = %s AND product_id = %s", (image_id,product_id))
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


def upload_product_images(image_location: str, product_id: int):
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


def delete_image_by_id(product_id: int,image_id: int):
    """
    Delete an image by its ID and associated product ID.

    Parameters:
        product_id (int): The ID of the product the image belongs to.
        image_id (int): The ID of the image to delete.
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


def delete_images_by_product_id(product_id: int):
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
