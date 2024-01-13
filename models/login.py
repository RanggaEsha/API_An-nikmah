from db import conn


def login_process(email: str, password: str):
    cur = conn.cursor()
    try:
        cur.execute('SELECT first_name,last_name,email,password FROM users WHERE email = %s AND password = %s', (email, password))
        user = cur.fetchone()
        if user:
            return {"username" : "%s %s" % (user[0],user[1])}
    finally:
        cur.close()

    return None




    