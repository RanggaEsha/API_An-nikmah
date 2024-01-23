from db import conn
from datetime import datetime


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


def get_transactions_by_user_id(user_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
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


def add_transaction(user_id, address, fullname, phone_number):
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO transactions (user_id,address,fullname,phone_number,created_at) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (user_id, address, fullname, phone_number, datetime.now()),
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
                    "quantity": item[3],
                    "price": item[4],
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


def get_transaction_details_by_user_id_and_product_id(transaction_id, product_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id,user_id,product_id,quantity FROM treansaction_details WHERE user_id = %s AND product_id=%s",
            (transaction_id, product_id),
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


def add_transaction_details(transaction_id, product_id, quantity, price):
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO transaction_details (transaction_id,product_id,quantity,price) VALUES (%s,%s,%s,%s)",
            (transaction_id, product_id, quantity, price),
        )
    except Exception as e:
        raise e
    finally:
        cur.close()
