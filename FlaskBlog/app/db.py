# -*- coding:utf-8 -*-
from tinydb import TinyDB, Query
import ujson

def get_db():
    db = TinyDB('db.json')
    return db

def get_table(table_name):
    table = get_db().table(table_name)
    return table

def get_record(table_name, query):
    res = get_table(table_name).get(query)
    return res

def search_records(table_name, query):
    res = get_table(table_name).search(query)
    return res

def insert_record(table_name, record):
    element_id = get_table(table_name).insert(record)
    return element_id

def update_record(table_name, field, query):
    get_table(table_name).update(field, query)
    return True

def get_element_id(table_name, query):
    element = get_record(table_name,query)
    element_id = element.eid
    element_doc_id = element.doc_id
    return element_id

