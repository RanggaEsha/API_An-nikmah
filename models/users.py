from db import conn
from flask_bcrypt import Bcrypt 

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
    Find a user by email and password.

    Parameters:
    - email (str): The email address of the user.
    - password (str): The password provided by the user.

    Returns:
    - dict or None: A dictionary containing user information including user ID, username, and role if the email and password match, otherwise None.

    Note:
    - This function retrieves user information from the database based on the provided email address.
    - It then compares the hashed password stored in the database with the provided password using bcrypt hashing.
    - If the password matches, it returns a dictionary containing user ID, username (combination of first name and last name), and role.
    - If no user is found with the provided email or if the password does not match, it returns None.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT id, first_name, last_name, email, password, role FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        if user:
            # Extract the hashed password from the database
            hashed_password = user[4]
            # Initialize bcrypt for password comparison
            bcrypt = Bcrypt()
            # Compare the hashed password from the database with the provided password using bcrypt hashing
            if bcrypt.check_password_hash(hashed_password, password):
                # If the password matches, construct a dictionary with user information
                return {
                    "id": user[0],
                    "username": user[1] + " " + user[2],  # Combine first name and last name to form the username
                    "role": user[5]
                }
        else:
            return None
    except Exception as e:
        raise e
    finally:
        cur.close()
    


def add_user_data(first_name: str, last_name, email, password):
    """
    Add user data to the database.

    Parameters:
    - first_name (str): The first name of the user.
    - last_name (str): The last name of the user.
    - email (str): The email address of the user.
    - password (str): The password provided by the user.

    Returns:
    - None

    Note:
    - This function adds user data to the database.
    - It hashes the provided password using bcrypt before storing it in the database.
    - The role of the user is set to "user" by default.
    """
    cur = conn.cursor()
    try:
        # Initialize bcrypt for password hashing
        bcrypt = Bcrypt()
        # Hash the provided password using bcrypt and decode it to utf-8 format
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute('INSERT INTO users (first_name, last_name, email, password, role) VALUES (%s, %s, %s, %s, %s)',
                    (first_name, last_name, email, hashed_password, "user"))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def add_admin_data(first_name,last_name,email,password):
    cur = conn.cursor()
    try:
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute('INSERT INTO users (first_name,last_name,email,password,role) VALUES (%s,%s,%s,%s,%s)',(first_name,last_name,email,hashed_password,"admin"))
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

def get_user_data(id: int):
    """
    Retrieve user data from the database by user ID.

    Parameters:
    - id (int): The ID of the user whose data is to be retrieved.

    Returns:
    - dict or None: A dictionary containing user information including first name, last name, email, and hashed password if the user is found, or None if the user ID is not found.

    Note:
    - This function retrieves user data from the database based on the provided user ID.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT first_name, last_name, email, password, role FROM users WHERE id = %s', (id,))
        user = cur.fetchone()
        if user:
            # Create a dictionary containing user information
            data = {
                "first_name": user[0],
                "last_name": user[1],
                "email": user[2],
                "password": user[3]  # Note: Password is hashed and stored in the database
            }
            return data
        else:
            return None
    finally:
        cur.close()


def update_data_user(id, first_name, last_name, email, password):
    """
    Update user data in the database.

    Parameters:
    - id (int): The ID of the user whose data will be updated.
    - first_name (str): The new first name for the user.
    - last_name (str): The new last name for the user.
    - email (str): The new email address for the user.
    - password (str): The new password for the user.

    Returns:
    - None

    Note:
    - This function updates the user data in the database based on the provided user ID.
    """
    cur = conn.cursor()
    try:
        cur.execute('''
                    UPDATE users
                    SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    password = %s
                    WHERE id = %s''', (first_name, last_name, email, password, id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_user(id: int):
    """
    Delete a user from the database.

    Parameters:
    - id (int): The ID of the user to be deleted.

    Returns:
    - None

    Note:
    - This function deletes a user from the database based on the provided user ID.
    """
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM users WHERE id = %s', (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    


    