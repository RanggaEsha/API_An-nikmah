from db import conn

# def product_category_id_validator(category_id):
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT * FROM products where category_id=%s", (category_id,))
#         if cur.fetchone():
#             return True
#     except Exception as e:
#         raise e
#     finally:
#         cur.close()




