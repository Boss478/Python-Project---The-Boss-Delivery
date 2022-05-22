import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter as tk

conn = sqlite3.connect("project.db")
c = conn.cursor()


class Registration:
    def engAlphaCheck(text):
        check = True
        for i in text:
            if "A" <= i <= "Z" or "a" <= i <= "z":
                pass
            else:
                check = False
        return check
    def engAlphaNumCheck(text):
        check = True
        for i in text:
            if "A" <= i <= "Z" or "a" <= i <= "z" or "0" <= i <= "9":
                pass
            else:
                check = False
        return check
    def engAlphaNumSymCheck(text):
        check = True
        for i in text:
            if "A" <= i <= "Z" or "a" <= i <= "z" or "0" <= i <= "9" or i == '_' or i == '-':
                pass
            else:
                check = False
        return check
    def dataCheck(fname,lname,phone):
        if phone.isnumeric() and len(phone) == 10:
            if Registration.engAlphaCheck(fname) and Registration.engAlphaCheck(lname):
                return True
            else:
                tkinter.messagebox.showerror('ERROR','ชื่อ-สกุลต้องเป็นตัวอักษร(ภาษาอังกฤษ)เท่านั้น')
                return False
        else:
            tkinter.messagebox.showerror('ERROR','เบอร์โทรศัพท์ไม่ถูกต้อง')
            return False
    def add(username,password,fname,lname,phone):
        if Registration.checkUsername(username) == False:
            if Registration.engAlphaNumSymCheck(username) == True:
                if Registration.dataCheck(fname,lname,phone) == True:
                    if len(password) > 6:
                        confirm = tkinter.messagebox.askquestion('CONFIRM','คุณยืนยันที่จะสมัครสมาชิกหรือไม่\n"โปรดตรวจสอบข้อมูลก่อน"')
                        if confirm == 'yes':
                            try:
                                access = 'MEMBER'
                                d = (username,password,fname,lname,phone,access)
                                c.execute('INSERT INTO users (username,password,fname,lname,phone,access) VALUES (?,?,?,?,?,?)',d)
                                conn.commit()
                                tkinter.messagebox.showinfo('SUCCEED','สมัครสมาชิกเรียบร้อยแล้ว')
                                return True
                            except sqlite3.Error as e:
                                tkinter.messagebox.showwarning('ERROR', 'พบข้อผิดพลาด\n({})'.format(e))
                                print(e)
                                return False
                        else:
                            return False
                    else:
                        tkinter.messagebox.showerror('ERROR', 'รหัสผ่านต้องมีมากกว่า 6 ตัวอักษร')
                        return False
            else:
                tkinter.messagebox.showerror('ERROR','ชื่อผู้ใช้ต้องเป็นภาษาอังกฤษเท่านั้น')
                return False
        else:
            tkinter.messagebox.showerror('ERROR','ชื่อผู้ใช้นี้ถูกใช้ไปแล้ว')
            return False
    def getAllUsername():
        c.execute('SELECT username FROM users')
        result = c.fetchall()
        usernameList = []
        for i in range(len(result)):
            usernameList.append(result[i][0])
        return usernameList
    def getAllIDs():
        c.execute('SELECT id FROM users')
        result = c.fetchall()
        ids = []
        for i in range(len(result)):
            ids.append(result[i][0])
        return ids
    def checkUsername(username):
        usernameList = Registration.getAllUsername()
        if username in usernameList:
            return True
        else:
            return False
    def checkID(id):
        idList = Registration.getAllIDs()
        if id in idList:
            return True
        else:
            return False
    def getDataID(id):
        c.execute('SELECT * FROM users WHERE id = ?',(id,))
        result = c.fetchall()
        return result[0] # Tuples # (id,username,password,fname,lname,phone,access)
    def getDataUsername(username):
        c.execute('SELECT * FROM users WHERE username = ?',(username,))
        result = c.fetchall()
        return result[0] # Tuples # (0 id, 1 username, 2 password, 3 fname, 4 lname, 5 phone, 6 access)
    def getName(username):
        fname = Registration.getDataUsername(username)[3]
        lname = Registration.getDataUsername(username)[4]
        name = fname + ' ' + lname
        return name
    def getPhone(username):
        return Registration.getDataUsername(username)[5]
    def getAccessID(id):
        return Registration.getDataID(id)[6]
    def getAccessUsername(username):
        return Registration.getDataUsername(username)[6]
    def changeAccess(username, access):
        if Registration.checkUsername(username) == True:
            confirm = tkinter.messagebox.askquestion('CONFIRM','คุณยืนยันที่จะปรับสิทธิของ {} หรือไม่'.format(username))
            if confirm == 'yes':
                try:
                    d = (access.upper(),username)
                    c.execute('''UPDATE users SET access = ? WHERE username = ?''', d)
                    conn.commit()
                    tkinter.messagebox.showinfo('SUCCEED','แก้ไขข้อมูลของ {} เรียบร้อยแล้ว'.format(username,d))
                    # print('ทำการแก้ไขข้อมูลของ {} เรียบร้อยแล้ว! {}'.format(username,d))
                    return True
                except sqlite3.Error as e:
                    print(e)
                    tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด\n({})'.format(e))
                    return False
            else:
                return False
        else:
            tkinter.messagebox.showerror('ERROR','ไม่พบชื่อผู้ใช้นี้')
            return False
    def edit(id,fname,lname,phone):
        if Registration.checkID(id) == True:
            if Registration.dataCheck(fname,lname,phone) == True:
                confirm = tkinter.messagebox.askquestion('CONFIRM','คุณยืนยันที่จะแก้ไขข้อมูลหรือไม่\n"โปรดตรวจสอบข้อมูลก่อน"')
                if confirm == 'yes':
                    try:
                        d = (fname,lname,phone,id)
                        c.execute('''UPDATE users SET fname = ?, lname = ?, phone = ? WHERE id = ?''', d)
                        conn.commit()
                        tkinter.messagebox.showinfo('SUCCEED','แก้ไขข้อมูลเรียบร้อยแล้ว')
                        # print('ทำการแก้ไขข้อมูลของ {} เรียบร้อยแล้ว! {}'.format(id,d))
                        return True
                    except sqlite3.Error as e:
                        print(e)
                        tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด\n({})'.format(e))
                        return False
                else:
                    return False
        else:
            tkinter.messagebox.showerror('ERROR','ไม่พบชื่อผู้ใช้นี้')
            return False
    def changePassword(id, newpassword):
        if Registration.checkID(id) == True:
            oldPassword = Registration.getDataID(id)[2]
            if len(newpassword) > 6 and newpassword != oldPassword:
                try:
                    d = (newpassword,id)
                    c.execute('UPDATE users SET password = ? WHERE id = ?', d)
                    conn.commit()
                    tkinter.messagebox.showinfo('SUCCEED','เปลี่ยนรหัสผ่านเรียบร้อยแล้ว')
                    # print(id, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว!')
                    return True
                except sqlite3.Error as e:
                    print(e)
                    tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด\n({})'.format(e))
                    return False
            else:
                tkinter.messagebox.showerror('ERROR','รหัสผ่านใหม่ต้องมากกว่า 6 ตัวอักษร\nและต้องไม่ซ้ำกับรหัสเดิม')
                return False
        else:
            tkinter.messagebox.showerror('ERROR','ไม่พบชื่อผู้ใช้นี้')
            return False
    def login(username,password):
        if Registration.checkUsername(username) == True:
            userPassword = Registration.getDataUsername(username)[2]
            if password == userPassword:
                tkinter.messagebox.showinfo('SUCCEED','เข้าสู่ระบบเรียบร้อยแล้ว')
                return True
            else:
                tkinter.messagebox.showerror('ERROR','รหัสผ่านไม่ถูกต้อง')
                return False
        else:
            tkinter.messagebox.showerror('ERROR','ไม่พบชื่อผู้ใช้นี้')
            return False