import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def execute_query(sql, params=()):
    conn = sqlite3.connect('db_Supermarket_FacundoMartin.db')
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.fetchall()
    except Exception as e:
        print(e)
    conn.close()
    return result

def create_productos_table():
    sql = '''CREATE TABLE IF NOT EXISTS productos(
             producto_id INTEGER PRIMARY KEY,
             nombre VARCHAR(70) NOT NULL,
             precio VARCHAR(50) NOT NULL,
             stock VARCHAR(50) NOT NULL
             )'''
    execute_query(sql)

def create_ventas_table():
    sql = '''CREATE TABLE IF NOT EXISTS ventas(
             venta_id INTEGER PRIMARY KEY AUTOINCREMENT,
             producto VARCHAR(50) NOT NULL,
             precio VARCHAR(70) NOT NULL,
             cantidad VARCHAR(50) NOT NULL,
             subtotal VARCHAR(50) NOT NULL,
             cerrada INTEGER DEFAULT 0 NOT NULL
             )'''
    execute_query(sql)

def create_reportes_table():
    sql = '''CREATE TABLE IF NOT EXISTS reportes(
             reporte_id INTEGER PRIMARY KEY AUTOINCREMENT,
             detalle VARCHAR(100) NOT NULL,
             fecha VARCHAR(50) NOT NULL,
             hora VARCHAR(50) NOT NULL,
             total VARCHAR(50) NOT NULL
             )'''
    execute_query(sql)

create_productos_table()
create_ventas_table()
create_reportes_table()