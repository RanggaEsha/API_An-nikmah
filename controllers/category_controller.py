from flask import request 
from models import *

def get_categories_controller():
    return get_categories()

def get_category_controller(id):
    if category_id_validator(id) is None:
        return {'message':'ID kategori tidak ditemukan'},404
    return get_category(id)

def add_category_controller():
    name = request.form.get('name')
    add_category(name)
    return {'message':'kategori berhasil ditambahkan'},200

def update_category_controller(id):
    name = request.form.get('name')
    if category_id_validator(id) is None:
        return {'message':'ID kategori tidak ditemukan'},404
    update_category(id,name)
    return {'message':'ID kategori berhasil diubah'},200


def delete_category_controller(id):
    if category_id_validator(id):
        delete_category(id)
        return {'message':'kategori berhasil dihapus'},200
    return {"message": "ID kategori tidak ditemukan"},404