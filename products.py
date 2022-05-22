import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter as tk

conn = sqlite3.connect('project.db')
c = conn.cursor()

class Product:
    def add(name, price):
        if Product.check(name) == False:
            try:
                c.execute('''INSERT INTO products (name, price) VALUES (?,?)''', (name,price))
                conn.commit()
                tkinter.messagebox.showinfo('COMPLETED','เพิ่มสินค้า "{}" ในราคา (฿{}) สำเร็จ!'.format(name,price))
                # print('เพิ่มสินค้า "{}" ในราคา (฿{}) สำเร็จแล้ว!'.format(name,price)) 
            except sqlite3.Error as e:
                print(e)
                tkinter.messagebox.showwarning('ERROR', e)
        else:
            tkinter.messagebox.showerror('ERROR','มีสินค้า "{}" ในฐานข้อมูลอยู่แล้ว!'.format(name))
    def edit(name, price):
        if price <= 0:
            tkinter.messagebox.showerror('ERROR','ราคาต้องมากกว่า 0')
            return False
        else:
            if Product.check(name) == True:
                try:
                    oldPrice = Product.getPrice_name(name)
                    c.execute('''UPDATE products SET price = ? WHERE name = ?''', (price,name))
                    conn.commit()
                    tkinter.messagebox.showinfo('COMPLETE','ทำการแก้ไข {} เรียบร้อยแล้ว\n(จาก {} เป็น {})'.format(name,oldPrice,price))
                    # print('ทำการแก้ไขราคาของ {} จาก ฿{} เป็น ฿{} เรียบร้อยแล้ว!'.format(name,oldPrice,price))
                    return True
                except sqlite3.Error as e:
                    tkinter.messagebox.showerror('ERROR', 'ไม่สามารถดำเนินการได้\n({})'.format(e))
                    return False
            else:
                tkinter.messagebox.showerror('ERROR','ไม่พบสินค้าที่ต้องการแก้ไข')
                return False
    def remove(name):
        if Product.check(name) == True:
            id = Product.getID(name)
            try:
                confirm = tkinter.messagebox.askquestion('CONFIRM','คุณจะลบ "{}" หรือไม่!'.format(name))
                if confirm == 'yes':
                    c.execute('''DELETE FROM products WHERE productid = ?''', (id,))
                    conn.commit()
                    # print('ลบสินค้า "{} {}" สำเร็จแล้ว!'.format(id,name))   
                    tkinter.messagebox.showinfo('COMPLETE','ลบสินค้า "{}" สำเร็จแล้ว!'.format(name))
                    return True
            except sqlite3.Error as e:
                tkinter.messagebox.showerror('ERROR', 'ไม่สามารถดำเนินการได้\n({})'.format(e))
                return False
        else:
            tkinter.messagebox.showerror('ERROR','ไม่พบสินค้า!')
            return False 
    def showAll(): # แก้-จัดคำ
        c.execute('SELECT * FROM products')
        result = c.fetchall()
        print('{:<3} {:<25} {:<10}'.format('ID', 'Product', 'Price'))
        for i in range(len(result)):
            print('{:<3} {:<25} ฿{:<10,.2f}'.format(result[i][0], result[i][1], result[i][2]))
    def getAllProducts():
        c.execute('SELECT name FROM products')
        result = c.fetchall()
        productList = []
        for i in range(len(result)):
            productList.append(result[i][0])
        return productList
    def getAllID():
        c.execute('SELECT productid FROM products')
        result = c.fetchall()
        IDs = []
        for i in range(len(result)):
            IDs.append(result[i][0])
        return IDs
    def check(product):
        p = Product.getAllProducts()
        if product in p:
            return True
        else:
            return False
    def checkID(id):
        ids = Product.getAllID()
        if id in ids:
            return True
        else:
            return False
    def getNameID(id):
        c.execute('SELECT name FROM products WHERE productid = ?', (id,))
        result = c.fetchall()
        return str(result[0][0])
    def getID(name):
        c.execute('SELECT productid FROM products WHERE name = ?', (name,))
        result = c.fetchall()
        return int(result[0][0])
    def getPrice(id):
        c.execute('SELECT price FROM products WHERE productid = ?', (id,))
        result = c.fetchall()
        return float(result[0][0])
    def getPrice_name(name):
        c.execute('SELECT price FROM products WHERE name = ?', (name,))
        result = c.fetchall()
        if name == '*Cancelled*':
            return 0
        else:
            return float(result[0][0])