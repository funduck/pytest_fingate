"""Работа с БД, используемой в тестах"""

import psycopg2
import psycopg2.extras
import configparser

conn = None

def get_connection():
    """Возвращает коннект с БД, используемой в тестах"""
    global conn
    if conn is None:
        connect()
    return conn

def connect():
    """Соединение с БД, используемой в тестах"""
    global conn
    cfg = configparser.ConfigParser()
    cfg.read('db.ini')
    cfg = cfg["db"]
    conn = psycopg2.connect(database=cfg["database"], user=cfg["user"], password=cfg["password"], host=cfg["host"], port=cfg["port"])

def disconnect():
    """Закрывает соединение с БД, используемой в тестах"""
    global conn
    if conn is not None:
        conn.close()
        conn = None

def cursor():
    """Возвращает курсор с именоваными полями
    Соединяется с БД если надо
    Заменяет все танцы с 
      conn = psycopg2.connect(...)
      conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    """
    return get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor)
