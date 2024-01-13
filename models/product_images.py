from db import conn


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
                (image, product_id, id),
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
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
