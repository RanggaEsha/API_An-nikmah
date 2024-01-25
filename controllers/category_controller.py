from flask import request 
from models import *
from flask_jwt_extended import (get_jwt_identity)
from errors import *


def get_categories_controller():
    """
    Controller function to retrieve all categories.

    Returns:
    - list: A list containing dictionaries with category information including category ID and name.
    """
    return get_categories()

def get_category_controller(id: int):
    """
    Controller function to retrieve a category by category ID.

    Parameters:
    - id (int): The ID of the category to be retrieved.

    Returns:
    - dict or None: A dictionary containing category information including category ID and name if the category is found, or an error message with a 404 status code if the category ID is not found.
    """
    try:
        if get_category(id) is None:
            raise ValueError('ID kategori tidak ditemukan')
        return get_category(id)
    except ValueError as e:
         return {"message": str(e)},422
    except Exception as e:
         raise {"message":"inputan anda salah"}
def add_category_controller():
    """
    Controller function to add a new category.

    Returns:
    - dict: A dictionary containing a success message if the category is added successfully, or an error message with a 404 status code if the category name is already registered.
    """
    try:
        current_user = get_jwt_identity()
        print(current_user)
        if current_user['role'] != 'admin':
            raise Unauthorized('Unauthorized')
        name = request.form.get('name')
        if get_category_name(name):
            raise DatabaseError('Nama kategori sudah terdaftar')
        add_category(name)
        return {'message':'kategori berhasil ditambahkan'},200
    except DatabaseError as e:
        return {"message": str(e)},404
    except Unauthorized as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return e

def update_category_controller(id: int):
    """
    Controller function to update a category.

    Parameters:
    - id (int): The ID of the category to be updated.

    Returns:
    - dict: A dictionary containing a success message if the category is updated successfully, or error messages with a 404 status code if the category ID is not found or the category name is already registered.
    """
    try:
        current_user = get_jwt_identity()
        print(current_user)
        if current_user['role'] != 'admin':
                raise Unauthorized('Unauthorized')
        name = request.form.get('name')
        if get_category(id) is None:
            raise DatabaseError('ID kategori tidak ditemukan')
        if get_category_name(name):
            raise DatabaseError('Nama kategori sudah terdaftar')
        update_category(id,name)
        return {'message':'Kategori berhasil diubah'},200
    except DatabaseError as e:
        return {"message": str(e)},404
    except Unauthorized as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422

def delete_category_controller(id):
    """
    Controller function to delete a category.

    Parameters:
    - id (int): The ID of the category to be deleted.

    Returns:
    - dict: A dictionary containing a success message if the category is deleted successfully, or an error message with a 404 status code if the category ID is not found.
    """
    try:
        current_user = get_jwt_identity()
        print(current_user)
        if current_user['role'] != 'admin':
                raise Unauthorized('Unauthorized')
        if get_category(id):
            delete_category(id)
            return {'message':'kategori berhasil dihapus'},200
        raise DatabaseError("ID kategori tidak ditemukan")
    except Unauthorized as ve:
        return {"message": str(ve)},422
    except DatabaseError as e:
        return {"message": str(e)},404
    except Exception as e:
        return {"message": str(e)},422