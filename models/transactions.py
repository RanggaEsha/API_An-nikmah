from db import conn
from datetime import datetime

def get_all_transactions(limit: int, page:int ,max_date: int,min_date: int):
    cur = conn.cursor()
    try:
        page = int(page)
        limit = int(limit)
        page = (page - 1) * limit
        where = []
        values = {"limit": limit, "offset": page}
        if max_date and min_date:
            where.append("created_at BETWEEN %(min_date)s AND %(max_date)s")
            values["min_date"] = min_date
            values["max_date"] = max_date
        elif min_date:
            where.append("created_at >= %(min_date)s")
            values["min_date"] = min_date
        elif max_date:
            where.append("created_at <= %(max_date)s")
            values["max_date"] = max_date
        if len(where) > 0:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ''

        query = (f"""
        SELECT * FROM transactions p {where}
        limit %(limit)s offset %(offset)s
        """)
        print(query,values)
        cur.execute(query,values)
        list_data = []
        data = cur.fetchall()
        if not data and page >= cur.rowcount:
            return {"data": []}
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "address": item[2],
                    "fullname": item[3],
                    "phone_number": item[4],
                    "created_at": item[5],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def get_transactions_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM transactions WHERE id = %s", (id,))
        data = cur.fetchall()
        list_data = []
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "address": item[2],
                    "fullname": item[3],
                    "phone_number": item[4],
                    "created_at": item[5],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_transactions_by_user_id(user_id: int,limit: int, page:int ,max_date: int,min_date: int):

    cur = conn.cursor()
    try:
        page = int(page)
        limit = int(limit)
        page = (page - 1) * limit
        where = []
        values = {"limit": limit, "offset": page}
        if max_date and min_date:
            where.append("created_at BETWEEN %(min_date)s AND %(max_date)s")
            values["min_date"] = min_date
            values["max_date"] = max_date
        elif min_date:
            where.append("created_at >= %(min_date)s")
            values["min_date"] = min_date
        elif max_date:
            where.append("created_at <= %(max_date)s")
            values["max_date"] = max_date
        if user_id:
            where.append("user_id = %(user_id)s")
            values["user_id"] = user_id
        else:
            where = ""
        if len(where) > 0:
                where = "WHERE " + " AND ".join(where)
        query = (f"""
        SELECT * FROM transactions p {where}
        limit %(limit)s offset %(offset)s
        """)
        print(query,values)
        cur.execute(query,values)
        list_data = []
        data = cur.fetchall()
        if not data and page >= cur.rowcount:
            return {"data": []}
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "user_id": item[1],
                    "address": item[2],
                    "fullname": item[3],
                    "phone_number": item[4],
                    "created_at": item[5],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def add_transaction(user_id, address, fullname, phone_number):
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO transactions (user_id,address,fullname,phone_number,created_at) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (user_id, address, fullname, phone_number, 'now()'),
        )
        return cur.fetchone()[0]
    except Exception as e:
        raise e
    finally:
        cur.close()


def delete_transaction_by_user_id(user_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE from transactions where user_id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_transaction_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE from transactions where id = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


# TRANSACTION DETAILS


def get_transaction_details_by_transaction_id(transaction_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM transaction_details WHERE transaction_id = %s",
            (transaction_id,),
        )
        data = cur.fetchall()
        list_data = []
        if data:
            for item in data:
                new_data = {
                    "id": item[0],
                    "transaction_id": item[1],
                    "product_id": item[2],
                    "product_price": item[3],
                    "quantity": item[4],
                    "sub_total": item[5],
                    "created_at": item[6],
                }
                list_data.append(new_data)
            return list_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_transaction_details_by_user_id_and_product_id(user_id, product_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM treansaction_details WHERE user_id = %s AND product_id=%s",
            (user_id, product_id),
        )
        conn.commit()
        data = cur.fetchone()
        if data is not None:
            new_data = {
                "id": data[0],
                "transaction_id": data[1],
                "product_id": data[2],
                "quantity": data[3],
                "price": data[4],
                "created_at": data[5],
            }
            return new_data
        else:
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def add_transaction_details(transaction_id, product_id, product_price, quantity, sub_total):
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO transaction_details (transaction_id,product_id,product_price,quantity,sub_total) VALUES (%s,%s,%s,%s,%s)",
            (transaction_id, product_id, product_price, quantity, sub_total),
        )
    except Exception as e:
        raise e
    finally:
        cur.close()
