from db import conn

def all_product_images(product_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT image FROM product_images where product_id = %s",(product_id,))
        images = cur.fetchall()

        list_images =[]
        for image in images:
            item = {
                "image":image
            }
            list_images.append(item)
        return list_images
        
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


def update_product_images(id, image_location, product_id):
    cur = conn.cursor()
    try:
        for image in image_location:
            cur.execute(
                "UPDATE product_images SET image=%s, product_id=%s WHERE id=%s",
                (image, product_id, id)
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