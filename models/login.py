from db import conn


def login(email: str,password: str):
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT email,password FROM users WHERE email = %s AND password = %s',(email,password))
        row = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    return row



    