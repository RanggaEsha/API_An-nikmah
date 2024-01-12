from db import conn


def login_process(email: str, password: str):
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cur.fetchone()
        if user:
            return {"email": user[2], "first_name": user[1]}
    finally:
        cur.close()

    return None




    