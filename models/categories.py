from db import conn

def get_categories():
    """
    Retrieve all categories.

    Returns:
    - list: A list containing dictionaries with category information including category ID and name.
        data = {
                "category_id":data[0],
                "name":data[1],
            }
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT id category_id,name,slug FROM categories")
        categories = cur.fetchall()
        list_categories = []
        for category in categories:
            item = {
                "category_id":category[0],
                "name":category[1],
            }
            list_categories.append(item)
        return list_categories
    except Exception as e:
        raise e
    finally:
        cur.close()

def get_category(id: int):
    """
    Retrieve category by category ID.

    Parameters:
    - id (int): The ID of the category to be retrieved.

    Returns:
    - dict or None: A dictionary containing category information including category ID and name if the category is found, or None if the category ID is not found.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT id AS category_id,name,slug FROM categories where id = %s ORDER BY category_id ASC",(id,))
        category = cur.fetchone()
        if category:
            item = {
                "category_id":category[0],
                "name":category[1],
            }
            return item           
    except Exception as e:
        raise e
    finally:
        cur.close()

def get_category_name(name: str):
    """
    Retrieve category by category name.

    Parameters:
    - name (str): The name of the category to be retrieved.

    Returns:
    - dict or None: A dictionary containing category information including category ID and name if the category is found, or None if the category name is not found.
    data = {
                "category_id":data[0],
                "name":data[1],
            }
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT id AS category_id,name,slug FROM categories where name = %s",(name,))
        category = cur.fetchone()

        if category:
            item = {
                "category_id":category[0],
                "name":category[1],
            }
            return item           
    except Exception as e:
        raise e
    finally:
        cur.close()

def add_category(name: str):
    """
    Add a new category to the database.

    Parameters:
    - name (str): The name of the new category.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name,slug) VALUES (%s,%s)",(name,name))
        conn.commit()          
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def update_category(id: int,name: str):
    """
    Update category information in the database.

    Parameters:
    - id (int): The ID of the category to be updated.
    - name (str): The new name for the category.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute("UPDATE categories SET name = %s, slug = %s where id = %s",(name,name,id))
        conn.commit()          
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_category(id: int):
    """
    Delete a category from the database.

    Parameters:
    - id (int): The ID of the category to be deleted.

    Returns:
    - None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE from categories where id = %s",(id,))
        conn.commit()         
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()