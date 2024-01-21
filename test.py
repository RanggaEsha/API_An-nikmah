keyword = "None"
category_id = "None"
page = 1
limit = 10


join = []
where = []

# where_and = " AND ".join()
if keyword is not None:
    where.append("name LIKE %(keyword)s")

if category_id is not None:
    where.append("category_id = %(category_id)s")
    join.append("JOIN categories on products.id = categories.product_id")

if len(where) > 0:
    where = "WHERE " + " AND ".join(where)

query = f"""
        SELECT * FROM products  
        {' '.join(join)} {where}
        limit %(limit)s offset %(offset)s
        """
print(query)
# where_and = " AND ".join(where)
# print(where_and)
# if len(where) > 0:
#     where_and = " WHERE " + where_andasd

# query = f"""

# SELECT * FROM products    {where_and} limit %(limit)s offset %(offset)s

# """

# print(query)
