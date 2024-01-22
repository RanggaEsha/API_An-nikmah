from db import conn

def get_user_id(id):
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM users WHERE id = %s', (id,))
        return cur.fetchone()
    except Exception as e:
        raise e
    finally:
        cur.close()

def find_email_password(email: str, password: str):
    cur = conn.cursor()
    try:
        cur.execute('SELECT id,first_name,last_name,email,password,role FROM users WHERE email = %s AND password = %s', (email, password))
        user = cur.fetchone()
        if user:
            return [{"id":user[0]},{"username":user[1]+" "+user[2]},{"role":user[5]}]
    finally:
        cur.close()
    return None

def add_user_data(first_name,last_name,email,password,role):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (first_name,last_name,email,password,role) VALUES (%s,%s,%s,%s,%s)',(first_name,last_name,email,password,role))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def find_email(request):
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



    