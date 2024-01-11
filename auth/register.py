import sys
sys.path.append('..')
from db import conn
from flask import request

def register1(request):
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (first_name,last_name,email,password) VALUES (%s,%s,%s,%s)',(first_name,last_name,email,password))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def validator_register(request):
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
