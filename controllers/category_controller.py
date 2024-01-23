from flask import request 
from models import *
from flask_jwt_extended import (get_jwt_identity)


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
    if get_category(id) is None:
        return {'message':'ID kategori tidak ditemukan'},404
    return get_category(id)

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
                return {'message':'Unauthorized'}, 401
        name = request.form.get('name')
        if get_category_name(name):
            return {'message':'Nama kategori sudah terdaftar'},404
        add_category(name)
        return {'message':'kategori berhasil ditambahkan'},200
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422

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
                return {'message':'Unauthorized'}, 401
        name = request.form.get('name')
        if get_category(id) is None:
            return {'message':'ID kategori tidak ditemukan'},404
        if get_category_name(name):
            return {'message':'Nama kategori sudah terdaftar'},404
        update_category(id,name)
        return {'message':'Kategori berhasil diubah'},200
    except ValueError as ve:
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
                return {'message':'Unauthorized'}, 401
        if get_category(id):
            delete_category(id)
            return {'message':'kategori berhasil dihapus'},200
        return {"message": "ID kategori tidak ditemukan"},404
    except ValueError as ve:
        return {"message": str(ve)},422
    except Exception as e:
        return {"message": str(e)},422