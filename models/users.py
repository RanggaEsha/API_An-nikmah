from db import conn

def get_user_id(id: int):
    """
    Retrieve user information by user ID.

    Parameters:
    - id (int): The ID of the user to be retrieved.

    Returns:
    - tuple or None: A tuple containing user information if the user is found, or None if the user ID is not found.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM users WHERE id = %s', (id,))
        return cur.fetchone()
    except Exception as e:
        raise e
    finally:
        cur.close()

def find_email_password(email: str, password: str):
    """
    Find user by email and password.

    Parameters:
    - email (str): Email of the user.
    - password (str): Password of the user.

    Returns:
    - list or None: A list containing user information (ID, username, and role) if the user is found, or None if the email and password combination is not valid.
    """
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
    """
    Add user data to the database.

    Parameters:
    - first_name (str): First name of the user.
    - last_name (str): Last name of the user.
    - email (str): Email of the user.
    - password (str): Password of the user.
    - role (str): Role of the user.

    Returns:
    - None
    """
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
    """
    Check if the email exists in the database.

    Parameters:
    - request (object): Flask request object containing form data.

    Returns:
    - bool: True if the email exists, False otherwise.
    """
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



    