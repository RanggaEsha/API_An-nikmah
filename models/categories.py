from db import conn

def get_categories():
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

def get_category(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id AS category_id,name,slug FROM categories where id = %s",(id,))
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

def add_category(name):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name,slug) VALUES (%s,%s)",(name,name))
        conn.commit()          
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def update_category(id,name):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE categories SET name = %s, slug = %s where id = %s",(name,name,id))
        conn.commit()          
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_category(id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE from categories where id = %s",(id,))
        conn.commit()         
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()