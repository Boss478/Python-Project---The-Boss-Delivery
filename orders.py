import sqlite3
import products
import ast
import datetime
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter as tk
import registration

conn = sqlite3.connect('project.db')
c = conn.cursor()

product = products.Product
register = registration.Registration

class Order:
    def add(date, username, address, orderList):
        if len(address) > 0:
            if len(orderList) > 0:
                confirm = tkinter.messagebox.askquestion('COMFIRM','คุณต้องการจะสั่งสินค้าหรือไม่')
                if confirm == 'yes':
                    try:
                        status = 'wait'
                        d = (date, username, address, str(orderList), status)
                        c.execute('''INSERT INTO userorders (date,username,address,orderlist,status) VALUES (?,?,?,?,?)''', d)
                        conn.commit()
                        # print('ทำการสั่งสินค้าเรียบร้อยแล้ว ข้อมูล : ', d)
                        tkinter.messagebox.showinfo('COMPLETE', 'สั่งซื้อสินค้าเรียบร้อยแล้ว')
                        return True
                    except sqlite3.Error as e:
                        print(e)
                        tkinter.messagebox.showerror('ERROR', 'พบข้อผิดพลาด\n({})'.format(e))
                        return False
            else:
                tkinter.messagebox.showerror('ERROR', 'คุณยังไม่ได้เพิ่มสินค้าใส่ตะกร้า')
                return False
        else:
            tkinter.messagebox.showerror('ERROR', 'โปรดกรอกข้อมูลให้ครบถ้วน')
            return False
    def showAllOrder():
        c.execute('SELECT * FROM userorders')
        result = c.fetchall()
        print('\n {:<2} {:<20} {:<26} {:<10}'.format('ID', 'Date', 'Name'))
        for i in range(len(result)):
            print(' {:<2} {:<20} {:<26} {:<10} {}'.format(result[i][0], result[i][2], result[i][1], result[i][3]))
    def getOrderListID(id):
        c.execute('SELECT orderlist FROM userorders WHERE id = ?', (id,))
        result = c.fetchall() # Tuples
        orderListTemp = result[0][0]
        orderList = ast.literal_eval(orderListTemp)
        return orderList # Dict
    def getOrderListID_list(id):
        orderList = Order.getOrderListID(id)
        orderProduct = []
        for x in orderList.keys():
            orderProduct.append(x)
        return orderProduct
    def getStatus(id):
        c.execute('SELECT status FROM userorders WHERE id = ?', (id,))
        result = c.fetchall()
        return result[0][0]
    def edit(id,orderList):
        if len(orderList) > 0:
            if Order.getStatus(id) == 'wait':
                confirm = tkinter.messagebox.askquestion('COMFIRM','คุณต้องการจะแก้ไขรายการสั่งซื้อหรือไม่')
                if confirm == 'yes':
                    try:
                        d = (str(orderList),id)
                        c.execute('''UPDATE userorders SET orderlist = ? WHERE id = ?''', d)           
                        conn.commit()
                        # print('ทำการแก้ไขรายการสั่งซื้อเรียบร้อยแล้ว ข้อมูล : ', d)
                        tkinter.messagebox.showinfo('COMPLETE', 'แก้ไขรายการสั่งซื้อเรียบร้อยแล้ว')
                        return True
                    except sqlite3.Error as e:
                        print(e)
                        tkinter.messagebox.showerror('ERROR', 'พบข้อผิดพลาด\n({})'.format(e))
                        return False
            else:
                tkinter.messagebox.showerror('ERROR', 'Order นี้ถูกยกเลิกแล้ว')
                return False
        else:
            tkinter.messagebox.showerror('ERROR','คุณยังไม่ได้เพิ่มสินค้าใส่ตะกร้า')
            return False
    def cancel(id):
        status = Order.getStatus(id)
        if status != 'cancelled' and status != 'delivered':
            confirm = tkinter.messagebox.askquestion('COMFIRM','คุณต้องการจะยกเลิกการสั่งซื้อหรือไม่')
            if confirm == 'yes':
                try:
                    d = ('cancelled',id)
                    c.execute('''UPDATE userorders SET status = ? WHERE id = ?''', d)           
                    conn.commit()
                    # print('ยกเลิกรายการสั่งซื้อ Order ID : ', d)
                    tkinter.messagebox.showinfo('COMPLETE', 'ยกเลิกการสั่งซื้อแล้ว')
                    return True
                except sqlite3.Error as e:
                    print(e)
                    tkinter.messagebox.showerror('ERROR', 'พบข้อผิดพลาด\n({})'.format(e))
                    return False
        else:
            tkinter.messagebox.showerror('ERROR', 'Order นี้ถูกยกเลิกแล้ว')
            return False
    def updateStatus(id, statusUpdate):
        status = Order.getStatus(id)
        if Order.check(id) == True:
            if status != 'cancelled' and status != 'delivered':
                confirm = tkinter.messagebox.askquestion('CONFIRM','คุณต้องการจะเปลี่ยนแปลงสถานะของรายการนี้หรือไม่')
                if confirm == 'yes':
                    try:
                        d = (statusUpdate, id)
                        c.execute('''UPDATE userorders SET status = ? WHERE id = ?''', d)
                        conn.commit()
                        # print('update status order {} to {}'.format(id, statusUpdate))
                        tkinter.messagebox.showinfo('SUCCEED','อัพเดทสถานะการสั่งซื้อแล้ว')
                        return True
                    except sqlite3.Error as e:
                        print(e)
                        tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด\n({})'.format(e))
                        return False
            else:
                tkinter.messagebox.showerror('ERROR','ไม่สามารถดำเนินการได้\nเนื่องจากรายการนี้ถูกยกเลิกหรือดำเนินการเรียบร้อยแล้ว')
        else:
            tkinter.messagebox.showerror('ERROR','ไม่พบรายการที่ต้องการ')
    def allID():
        c.execute('SELECT id FROM userorders')
        result = c.fetchall()
        ids = []
        for i in range(len(result)):
            ids.append(result[i][0])
        return ids
    def userListID(username):
        c.execute('SELECT id FROM userorders WHERE username = ?', (username,))
        result = c.fetchall()
        ids = []
        for i in range(len(result)):
            ids.append(result[i][0])
        return ids
    def check(id):
        ids = Order.allID()
        if id in ids:
            return True
        else:
            return False
    def checkName(name):
        c.execute('SELECT username FROM userorders')
        result = c.fetchall()
        names = []
        for i in range(len(result)):
            names.append(result[i][0])
        if name in names:
            return True
        else:
            return False
    def getName(id):
        c.execute('SELECT username FROM userorders WHERE id = ?', (id,))
        result = c.fetchall()
        return str(result[0][0])
    def getDate(id):
        c.execute('SELECT date FROM userorders WHERE id = ?', (id,))
        result = c.fetchall()
        return str(result[0][0])
    def getAddress(id):
        c.execute('SELECT address FROM userorders WHERE id = ?', (id,))
        result = c.fetchall()
        return str(result[0][0])
    def getPhone(username):
        c.execute('SELECT phone FROM users WHERE username = ?', (username,))
        result = c.fetchall()
        return str(result[0][0])
    def calculate(id):
        if Order.check(id) == True:
            orderList = Order.getOrderListID(id)
            status = Order.getStatus(id)
            total = 0
            distancePrice = 10
            for x, y in orderList.items():
                eachProductPrice = product.getPrice_name(x)
                productPrice = eachProductPrice * y
                total = total + productPrice
            total = total + distancePrice
        else:
            total = 0
            # print('Order ID :' + str(id) + ' is not found.')
        return total