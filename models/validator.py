from db import conn

def category_id_validator(category_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products where category_id=%s", (category_id,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()

def product_id_validator(product_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products where id=%s", (product_id,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()

def image_id_validator(image_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM product_images where id=%s", (image_id,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()

def image_product_id_validator(product_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM product_images where product_id=%s", (product_id,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()

def validator_register(request):
    email = request.form.get('email')
    
    cur = conn.cursor()
    try:
        cur.execute('SELECT email,password FROM users where email = %s', (email,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()