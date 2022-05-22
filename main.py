from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter as tk
import sqlite3
import datetime
import webbrowser
import products
import orders
import registration

product = products.Product
order = orders.Order
register = registration.Registration

conn = sqlite3.connect('project.db')
c = conn.cursor()

isLogin = False
userLogin = ''

def createDatabaseTable():
    try:
        c.execute('''CREATE TABLE products(productid integer PRIMARY KEY,
            name varchar(25) NOT NULL,
            price integer NOT NULL)''')
        conn.commit()
        c.execute('''CREATE TABLE users(id integer PRIMARY KEY,
            username varchar(30) NOT NULL,
            password text NOT NULL,
            fname varchar(30) NOT NULL,
            lname varchar(30) NOT NULL,
            phone varchar(10) NOT NULL,
            access varchar(20) NOT NULL)''')
        conn.commit()
        c.execute('''CREATE TABLE userorders(id integer PRIMARY KEY,
            date text NOT NULL,
            username varchar(30) NOT NULL,
            address text NOT NULL,
            orderlist text NOT NULL,
            status text NOT NULL)''')
        conn.commit()
    except:
        pass

def createAdmin():
    if register.checkUsername('admin') == False:
        access = 'STAFF'
        d = ('admin','123456789','Admin','Users','0000000000',access)
        c.execute('INSERT INTO users (username,password,fname,lname,phone,access) VALUES (?,?,?,?,?,?)',d)
        conn.commit()

def exit(main):
    confirm = tkinter.messagebox.askquestion('ยืนยัน','คุณต้องการจะออกจากโปรแกรมหรือไม่')
    if confirm == 'yes':
        main.destroy()
        conn.close()

def back(window):
    window.destroy()
    Main()

address = '193/77 16 ถนนกัลปพฤกษ์ ตำบลในเมือง \nอำเภอเมืองขอนแก่น ขอนแก่น 40000'
url = 'https://shorturl.at/almHT'

def Main():
    main = Tk()
    main.title('The Boss Delivery')
    main.geometry('600x600')
    main.configure(bg='#cac9bd')
    main.resizable(False, False)

    #Button Function
    def openEmployee():
        if isLogin == True:
            access = register.getAccessUsername(userLogin).upper()
            if access == 'STAFF':
                main.destroy()
                Employee()
            else:
                tkinter.messagebox.showerror('ERROR','คุณไม่มีสิทธิ์ที่จะเข้าสู่หน้านี้')
        else:
            tkinter.messagebox.showerror('ERROR','กรุณาเข้าสู่ระบบก่อน')
           
    def openCustomer():
        if isLogin == True:
            main.destroy()
            Customer()
        else:
            tkinter.messagebox.showerror('ERROR','กรุณาเข้าสู่ระบบก่อน')

    def openReg():
        main.destroy()
        registerFunc()

    def openLogin():
        main.destroy()
        loginFunc()

    def Logout():
        global isLogin
        global userLogin
        if isLogin == True:
            isLogin = False
            userLogin = ''
            tkinter.messagebox.showinfo('SUCCEED','ออกจากระบบเรียบร้อย')
        main.destroy()
        Main()

    def openProfile():
        if isLogin == True:
            profileFunc()
        else:
            tkinter.messagebox.showerror('ERROR','คุณยังไม่เข้าสู่ระบบ')

    def openInfo():
        infoWin = Tk()
        infoWin.title('รายละเอียดร้าน [The Boss Delivery]')
        infoWin.configure(bg='#FFEB6E')
        infoWin.resizable(False,False)
        
        Font = ("Tahoma", 15)
        FontBold = ("Tahoma Bold", 17)
        W = 40
        fg_grey = '#323232'
        info = Label(infoWin, text='  The Boss Delivery \n  รายละเอียด',font=FontBold,width=30,height=3,anchor='w',justify='left',bg='#BCF4FF',highlightthickness=5, highlightbackground="#776CFF").grid(row=1,column=0,sticky='w')
        time = Label(infoWin, text='เวลาที่เปิดทำการ: ',font=Font,width=W,height=1,anchor='w',bg='#FFEB6E').grid(row=2,column=0,sticky='w')
        time2 = Label(infoWin, text='ทุกวัน',font=Font,fg=fg_grey,width=W,height=2,anchor='w',justify="left",bg='white').grid(row=3,column=0,sticky='w')
        contact = Label(infoWin, text='เบอร์ติดต่อ: ',font=Font,width=W,height=1,anchor='w',bg='#FFEB6E').grid(row=4,column=0,sticky='w')
        contact2 = Label(infoWin, text='093-3948182',font=Font,fg=fg_grey,width=W,height=1,anchor='w',bg='white').grid(row=5,column=0,sticky='w')
        addressLb = Label(infoWin, text='ที่อยู่ร้าน: ',font=Font,width=W,height=1,anchor='w',bg='#FFEB6E').grid(row=6,column=0,sticky='w')
        address2 = Label(infoWin, text=address,font=Font,fg=fg_grey,width=W,height=2,anchor='w',justify="left",bg='white').grid(row=7,column=0,sticky='w')

    label1 = Button(main,text="The Boss Delivery",font=("Tahoma Bold",40),fg='black',bg='#f9f9f9',borderwidth=1,relief='solid',command=openInfo).place(x=0,y=-1,width=600,height=100)
    
    #Button
    loginText = ''
    if isLogin == True:
        access = register.getAccessUsername(userLogin).upper()
        if access == 'MEMBER':
            access = 'ผู้ใช้ทั่วไป'
        elif access == 'STAFF':
            access = 'พนักงาน'
        else:
            access = 'Unknown'
        loginText = 'Logged in as {} <{}>'.format(userLogin,access)
        profileButton = Button(main,text='ข้อมูลส่วนตัว',font=("Tahoma Bold",12),bg='white',fg='black',command=openProfile).place(x=380,y=98,width=110,height=45)
        logoutButton = Button(main,text='ออกจากระบบ',font=("Tahoma Bold",12),bg='#FF1919',fg='white',command=Logout).place(x=490,y=98,width=110,height=45)
    else:
        loginText = 'คุณยังไม่เข้าสู่ระบบ'
        loginButton = Button(main,text='เข้าสู่ระบบ',font=("Tahoma Bold",12),bg='#12A714',fg='white',command=openLogin).place(x=490,y=98,width=110,height=45)
        registerButton = Button(main,text='สมัครสมาชิก',font=("Tahoma Bold",12),bg='#147EDC',fg='white',command=openReg).place(x=380,y=98,width=110,height=45)
    
    def openMap():
        webbrowser.open(url)

    loginStatusLb = Label(main,text=loginText,font=("Tahoma",12),bg='white',borderwidth=1,relief='sunken').place(x=0,y=98)


    ctImageFile = PhotoImage(file = r"customers.png")
    ctImage = ctImageFile.subsample(2,2)
    locImageFile = PhotoImage(file = r"location.png")
    locImage = locImageFile.subsample(9,9)
    #employee = Button(main, text='สำหรับพนักงาน',font=("Tahoma",25),bg='#FF4040',command=openEmployee).place(x=140,y=500,width=300,height=60)
    loc = Button(main, text=address,image=locImage,compound=LEFT,font=("Tahoma",10),bg='white',command=openMap).place(x=115,y=500,width=350,height=60)
    customer = Button(main, text='เริ่มใช้งาน',image=ctImage,compound=TOP,font=("Tahoma",30),bg='#00FF1B',command=openCustomer).place(x=140,y=175,width=300,height=250)
    
    backImageFile = PhotoImage(file = r"exit.png")
    backImage = backImageFile.subsample(3,3)
    Button(main, image = backImage, font=("Tahoma",10),command=lambda: exit(main)).place(x=530,y=530,width=70,height=70)
    #Menu        
    MyMenu = Menu(main)
    # GO : พนักงาน ลูกค้า ออก
    menuItem = Menu(main)
    menuItem.add_command(label='หน้าต่างสำหรับพนักงาน',font=("Tahoma",10),command=openEmployee)
    menuItem.add_command(label='หน้าต่างสำหรับลูกค้า',font=("Tahoma",10),command=openCustomer)
    menuItem.add_command(label='ออกจากโปรแกรม',font=("Tahoma",10),command=lambda: exit(main))

    helpItem = Menu(main)
    helpItem.add_command(label='รายละเอียด',font=("Tahoma",10),command=openInfo)
    #Main Menu: GO
    MyMenu.add_cascade(label='Open',menu=menuItem)
    MyMenu.add_cascade(label='Help',menu=helpItem)
    main.config(menu=MyMenu)

    main.mainloop()

def profileFunc():
    profileWin = Tk()
    profileWin.title('ข้อมูลส่วนตัวของ {}'.format(userLogin))
    profileWin.geometry('400x500')
    profileWin.configure(bg='#cac9bd')
    profileWin.resizable(False,False)

    username = userLogin
    userData = register.getDataUsername(username)
    id = userData[0]
    password = userData[2]
    fname = userData[3]
    lname = userData[4]
    phone = userData[5]
    access = userData[6]

    Font = ("Tahoma",15)

    infoLb = Label(profileWin,text='ข้อมูลส่วนตัว',font=Font,bg='white',borderwidth=2,relief='solid').place(x=-2,y=-1,width=405,height=50)

    idLb = Label(profileWin,text=' User ID : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=60,width=150,height=30)
    idLbShow = Label(profileWin,text=id,font=Font,bg='#E7E7E7',borderwidth=1,relief='solid',anchor='w').place(x=151,y=60,width=50,height=30)
    accessLbShow = Label(profileWin,text=access,font=Font,bg='#E7E7E7',borderwidth=1,relief='solid').place(x=226,y=60,width=100,height=30)

    usernameLb = Label(profileWin,text=' ชื่อผู้ใช้ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=95,width=150,height=30)
    usernameLbShow = Label(profileWin,text=username,font=Font,bg='#E7E7E7',borderwidth=1,relief='solid',anchor='w').place(x=151,y=95,width=200,height=30)

    fnameLb = Label(profileWin,text=' ชื่อ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=130,width=150,height=30)
    fnameVar = StringVar(profileWin)
    fnameVar.set(fname)
    fnameEt = Entry(profileWin,textvariable=fnameVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=130,width=200,height=30)

    lnameLb = Label(profileWin,text=' นามสกุล : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=165,width=150,height=30)
    lnameVar = StringVar(profileWin)
    lnameVar.set(lname)
    lnameEt = Entry(profileWin,textvariable=lnameVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=165,width=200,height=30)

    phoneLb = Label(profileWin,text=' เบอร์โทรศัพท์ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=200,width=150,height=30)
    phoneVar = StringVar(profileWin)
    phoneVar.set(phone)
    phoneEt = Entry(profileWin,textvariable=phoneVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=200,width=200,height=30)

    curPwLb = Label(profileWin,text=' รหัสผ่านปัจจุบัน : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=235,width=150,height=30)
    currentPasswordVar = StringVar(profileWin)
    curPwEt = Entry(profileWin,textvariable=currentPasswordVar,font=Font,bg='white',borderwidth=1,relief='solid',show='*').place(x=151,y=235,width=240,height=30)

    newPwLb = Label(profileWin,text=' รหัสผ่านใหม่ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=265,width=150,height=30)
    newPasswordVar = StringVar(profileWin)
    newPwEt = Entry(profileWin,textvariable=newPasswordVar,font=Font,bg='white',borderwidth=1,relief='solid',show='*').place(x=151,y=265,width=240,height=30)

    hintLb = Label(profileWin,text='*สามารถแก้ไขข้อมูลได้เลย หลังจากนั้นกรอกรหัสผ่านเพื่อทำการแก้ไข\nหากไม่ต้องการเปลี่ยนรหัสผ่านให้ "เว้นว่าง" ไว้',font=("Tahoma",10)).place(x=0,y=310,width=400)

    def editData():
        curPassword = currentPasswordVar.get()
        newFName = fnameVar.get().capitalize()
        newLName = lnameVar.get().capitalize()
        newPhone = phoneVar.get()
        newPassword = newPasswordVar.get()
        if newFName == fname and newLName == lname and newPhone == phone and len(newPassword) == 0:
            profileWin.destroy()
        else:
            if curPassword == password:
                changePwSuccess = None
                changeDataSuccess = None
                if newFName != fname or newLName != lname or newPhone != phone:
                    changeDataSuccess = register.edit(id,newFName,newLName,newPhone)
                if len(newPassword) != 0:
                    changePwSuccess = register.changePassword(id,newPassword)
                if changeDataSuccess != False and changePwSuccess != False:
                    profileWin.destroy()
            else:
                tkinter.messagebox.showerror('ERROR','รหัสผ่านไม่ถูกต้อง')

    editButton = Button(profileWin,text='แก้ไขข้อมูล',font=("Tahoma Bold", 15),bg='#6AFF55',command=editData).place(x=125,y=425,width=150,height=50)

    profileWin.mainloop()

def registerFunc():
    registerWin = Tk()
    registerWin.title('สมัครสมาชิก')
    registerWin.geometry('400x500')
    registerWin.configure(bg='#cac9bd')
    registerWin.resizable(False, False)

    Font = ("Tahoma",15)

    regLb = Label(registerWin,font=("Tahoma Bold",15),text='  สร้างบัญชีของคุณ',anchor='w',bg='white',borderwidth=2,relief='solid').place(x=-1,y=-1,width=402,height=50)

    def registerAccount():
        username = usernameVar.get()
        password = passwordVar.get()
        cpassword = confirmPasswordVar.get()
        fname = fnameVar.get().capitalize()
        lname = lnameVar.get().capitalize()
        phone = phoneVar.get()

        if password == cpassword:
            success = register.add(username,password,fname,lname,phone)
            if success == True:
                global isLogin
                global userLogin
                registerWin.destroy()
                isLogin = True
                userLogin = username
                Main()
        else:
            tkinter.messagebox.showerror('ERROR','รหัสผ่านไม่เหมือนกัน')

    addBt = Button(registerWin,text='สมัครสมาชิก',font=('Tahoma Bold', 15),command=registerAccount,bg='#41B8F8').place(x=125,y=350,width=150,height=75)

    usernameVar = StringVar(registerWin)
    usernameEt = Entry(registerWin,textvariable=usernameVar,font=Font).place(x=0,y=85,width=400,height=25)
    usernameLb = Label(registerWin,text='ชื่อผู้ใช้: ',font=Font,anchor='w',bg='#cac9bd').place(x=0,y=60,width=400,height=25)
    
    fnameVar = StringVar(registerWin)
    nameLb = Label(registerWin,text="ชื่อ-สกุล (ภาษาอังกฤษ): ",font=Font,anchor='w',bg='#cac9bd').place(x=0,y=120,width=400,height=25)
    fnameEt = Entry(registerWin,textvariable=fnameVar,font=Font).place(x=0,y=145,width=199,height=25)

    lnameVar = StringVar(registerWin)
    lnameEt = Entry(registerWin,textvariable=lnameVar,font=Font).place(x=201,y=145,width=199,height=25)

    phoneVar = StringVar(registerWin)
    phoneLb = Label(registerWin,text="เบอร์โทรศัพท์: ",font=Font,anchor='w',bg='#cac9bd').place(x=0,y=180,width=400,height=25)
    phoneEt = Entry(registerWin,textvariable=phoneVar,font=Font).place(x=0,y=205,width=400,height=25)

    passwordVar = StringVar(registerWin)
    passwordLb = Label(registerWin,text="รหัสผ่าน: ",font=Font,anchor='w',bg='#cac9bd').place(x=0,y=240,width=400,height=25)
    passwordEt = Entry(registerWin,textvariable=passwordVar,font=Font,show='*').place(x=0,y=265,width=400,height=25)

    confirmPasswordVar = StringVar(registerWin)
    confirmPasswordLb = Label(registerWin,text="ยืนยันรหัสผ่าน",font=Font,anchor='w',bg='#cac9bd').place(x=0,y=290,width=400,height=25)
    confirmPasswordEt = Entry(registerWin,textvariable=confirmPasswordVar,font=Font,show='*').place(x=0,y=315,width=400,height=25)

    #Menu        
    MyMenu = Menu(registerWin)
    # GO : พนักงาน ลูกค้า ออก
    menuItem = Menu(registerWin)
    menuItem.add_command(label='หน้าแรก',font=("Tahoma",10),command=lambda: back(registerWin))
    #Main Menu: GO
    MyMenu.add_cascade(label='Open',menu=menuItem)
    registerWin.config(menu=MyMenu)

    registerWin.mainloop()

def loginFunc():
    loginWin = Tk()
    loginWin.title('เข้าสู่ระบบ')
    loginWin.configure(bg='#cac9bd')
    loginWin.geometry('300x300')
    loginWin.resizable(False, False)
    
    Font = ("Tahoma",13)

    LoginLb = Label(loginWin,font=("Tahoma Bold",15),text='เข้าสู่ระบบ',bg='white',borderwidth=2,relief='solid').place(x=-1,y=-1,width=302,height=50)

    def Login():
        username = usernameVar.get()
        password = passwordVar.get()
        if len(username) > 0 and len(password) > 0:
            success = register.login(username,password)
            if success == True:
                global isLogin
                global userLogin
                isLogin = True
                userLogin = username
                loginWin.destroy()
                Main()
        else:
            tkinter.messagebox.showerror('ERROR','ข้อมูลว่างเปล่า')

    addBt = Button(loginWin,text='เข้าสู่ระบบ',font=("Tahoma Bold", 15),command=Login,bg='#5BFF47').place(x=90,y=200,width=120,height=50)

    usernameVar = StringVar(loginWin)
    usernameEt = Entry(loginWin,textvariable=usernameVar,font=Font).place(x=0,y=85,width=300,height=25)
    usernameLb = Label(loginWin,text='ชื่อผู้ใช้: ',font=Font,bg='#cac9bd',anchor='w').place(x=0,y=60,width=300,height=25)

    passwordVar = StringVar(loginWin)
    passwordLb = Label(loginWin,text="รหัสผ่าน: ",font=Font,bg='#cac9bd',anchor='w').place(x=0,y=120,width=300,height=25)
    passwordEt = Entry(loginWin,textvariable=passwordVar,font=Font,show='*').place(x=0,y=145,width=300,height=25)

    #Menu        
    MyMenu = Menu(loginWin)
    # GO : พนักงาน ลูกค้า ออก
    menuItem = Menu(loginWin)
    menuItem.add_command(label='หน้าแรก',font=("Tahoma",10),command=lambda: back(loginWin))
    #Main Menu: GO
    MyMenu.add_cascade(label='Open',menu=menuItem)
    loginWin.config(menu=MyMenu)

    loginWin.mainloop()

def Employee():
    empWindow = Tk()
    empWindow.title('หน้าต่างสำหรับพนักงาน')
    empWindow.geometry('600x625')
    empWindow.configure(bg='grey')
    empWindow.resizable(False, False)

    def addFunc():
        addWin = Tk()
        addWin.resizable(False,False)
        
        def addProduct():
            try:
                n = name.get().upper()
                p = price.get()
                if "A" <= n <= "Z" or n == ' ':
                    if p > 0:              
                        product.add(n,p)
                        deleteText()
                        deletePrice()
                        show(empWindow,5,70,590,190)
                        
                    else:
                        tkinter.messagebox.showerror('ERROR','ราคาต้องมากกว่า 0')
                else:
                    tkinter.messagebox.showerror('ERROR','ชื่อสินค้ามีข้อผิดพลาด')
            except:
                tkinter.messagebox.showerror('ERROR', 'พบข้อผิดพลาด')  

        def backEmp():
            addWin.destroy()

        Label(addWin,text='ชื่อสินค้า (ภาษาอังกฤษ) ',font=("Tahoma",15),width=19,bg='white',anchor='e',borderwidth=1,relief='ridge').grid(row=0,column=0)
        Label(addWin,text='ราคาสินค้า ',font=("Tahoma",15),width=19,bg='white',anchor='e',borderwidth=1,relief='ridge').grid(row=1,column=0)
        
        name = StringVar(addWin)
        price = DoubleVar(addWin)
        nameEnt = Entry(addWin,font=("Tahoma",15),textvariable=name,width=35).grid(row=0,column=1,columnspan=3,sticky=W)

        priceEnt = Entry(addWin,font=("Tahoma",15),textvariable=price,width=35).grid(row=1,column=1,columnspan=3,sticky=W)

        def deleteText():
            name.set('')
        def deletePrice():
            price.set(0.0)

        clear = Button(addWin,text="ล้าง",font=("Tahoma",10),command=deleteText).grid(row=0,column=4,sticky=E)
        clear = Button(addWin,text="ล้าง",font=("Tahoma",10),command=deletePrice).grid(row=1,column=4,sticky=E)

        add = Button(addWin, text='เพิ่ม',font=("Tahoma",15),bg='#A1FF8F',command=addProduct,width=10).grid(row=5,column=3)
        back = Button(addWin, text='กลับ',font=("Tahoma",15),bg='yellow',command=backEmp,width=10).grid(row=5,column=0)

    def show(main,X,Y,W,H):
        tree = ttk.Treeview(main, column=("c1", "c2", "c3"), show='headings')
        tree.column("c1", anchor=CENTER)
        tree.heading("c1", text="ID")
        tree.column("c2", anchor=CENTER)
        tree.heading("c2", text="Product")
        tree.column("c3", anchor=CENTER)
        tree.heading("c3", text="Price")
        tree.place(x=X, y=Y, width=W, height=H)

        c.execute('SELECT * FROM products')
        result = c.fetchall()
        for row in result:
            #print(row)
            tree.insert("",tkinter.END,values=row)
        
    def edit():
        editData = Tk()
        editData.title('แก้ไขสินค้า')
        editData.geometry('355x170')
        editData.resizable(False, False)
        Label(editData,text='สินค้า',font=("Tahoma",15),bg='white',borderwidth=1,relief='ridge',width=10,anchor='e').grid(row=0,column=0)
        productList = StringVar(editData,value='...เลือกสินค้า...')
        nameList = ttk.Combobox(editData,font=("Tahoma",15),textvariable=productList)
        nameList["values"] = product.getAllProducts()
        nameList.grid(row=0,column=1)
        Label(editData,text='ราคาสินค้า',font=("Tahoma",15),borderwidth=1,relief='ridge',width=10,anchor='e').grid(row=1,column=0)
        price = DoubleVar(editData)
        priceEnt = Entry(editData,font=("Tahoma",15),textvariable=price)
        priceEnt.grid(row=1,column=1,sticky=W)

        def backEmp():
            editData.destroy()

        exitImageFile = PhotoImage(master=editData,file = r"exit.png")
        exitImage = exitImageFile.subsample(5,5)
        exitButton = Button(editData,image=exitImage,anchor='w',command=backEmp).place(x=0,y=120)

        def editProductFunc():
            try:
                editProduct = productList.get().upper()
                editPrice = price.get()
                success = product.edit(editProduct,editPrice)
                if success == True:
                    productList.set('...เลือกสินค้า...')
                    price.set(0.0)
                    show(empWindow,5,70,590,190)
            except:
                tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด')

        def remove():
            editProduct = productList.get().upper()
            success = product.remove(editProduct)
            if success == True:
                editData.destroy()   
        editButton = Button(editData, text='แก้ไข',font=("Tahoma",15),bg='orange',command=editProductFunc,width=7).grid(row=3,column=1)
        removeButton = Button(editData, text='ลบ',font=("Tahoma",15),bg='red',command=remove,width=7).grid(row=3,column=0)
        editData.mainloop()

    def showallorder(main,X,Y,W,H):
        tree = ttk.Treeview(main, column=("c1", "c2", "c3","c4"), show='headings')
        tree.column("c1", anchor=CENTER, minwidth=0, width=20)
        tree.heading("c1", text="ID")
        tree.column("c2", anchor=CENTER, minwidth=0, width=150)
        tree.heading("c2", text="DATE")
        tree.column("c3", anchor=CENTER, minwidth=0, width=200)
        tree.heading("c3", text="Username")
        tree.column("c4", anchor=CENTER, minwidth=0, width=100)
        tree.heading("c4", text="Status")
        tree.place(x=X,y=Y,width=W,height=H)

        c.execute('SELECT id,date,username,status FROM userorders')
        result = c.fetchall()
        for row in result:
            #print(row)
            tree.insert("",tkinter.END,values=row)

    def showallusers(main,X,Y,W,H):
        tree = ttk.Treeview(main, column=("c1", "c2", "c3","c4", "c5", "c6"), show='headings')
        tree.column("c1", anchor=CENTER, minwidth=0, width=20)
        tree.heading("c1", text="ID")
        tree.column("c2", anchor=CENTER, minwidth=0, width=50)
        tree.heading("c2", text="Username")
        tree.column("c3", anchor=CENTER, minwidth=0, width=50)
        tree.heading("c3", text="First Name")
        tree.column("c4", anchor=CENTER, minwidth=0, width=50)
        tree.heading("c4", text="Last Name")
        tree.column("c5", anchor=CENTER, minwidth=0, width=50)
        tree.heading("c5", text="Phone Number")
        tree.column("c6", anchor=CENTER, minwidth=0, width=50)
        tree.heading("c6", text="Access")
        tree.place(x=X,y=Y,width=W,height=H)

        c.execute('SELECT id,username,fname,lname,phone,access FROM users')
        result = c.fetchall()
        for row in result:
            #print(row)
            tree.insert("",tkinter.END,values=row)
    
    def updateUser():
        updateUserWin = Tk()
        updateUserWin.title('แก้ไขและแสดงข้อมูลผู้ใช้')
        updateUserWin.resizable(False, False)

        Label(updateUserWin,text='ชื่อผู้ใช้',font=("Tahoma",15),borderwidth=1,relief='ridge',width=10,anchor='e').grid(row=1,column=0)
        usernameVar = StringVar(updateUserWin,value='<เลือกผู้ใช้>')
        usernameList = ttk.Combobox(updateUserWin,font=("Tahoma",15),textvariable=usernameVar)
        usernameList["values"] = register.getAllUsername()
        usernameList.grid(row=1,column=1)
        def editAccessFunc():
            username = usernameVar.get()
            access = accessSet.get().upper()
            if access == 'MEMBER' or access == 'STAFF':
                success = register.changeAccess(username,access)
            else:
                tkinter.messagebox.showerror('ERROR','ไม่พบสิทธิ์ที่ต้องการแก้ไข')
        
        def editUser():
            updateUserWin.destroy()
            username = usernameVar.get()

            showUserWin = Tk()
            showUserWin.title('ข้อมูลของ {}'.format(username))
            showUserWin.geometry('400x500')
            showUserWin.configure(bg='#cac9bd')
            showUserWin.resizable(False,False)

            userData = register.getDataUsername(username)
            id = userData[0]
            password = userData[2]
            fname = userData[3]
            lname = userData[4]
            phone = userData[5]
            access = userData[6]

            Font = ("Tahoma",15)

            infoLb = Label(showUserWin,text='ข้อมูลของ {}'.format(username),font=Font,bg='white',borderwidth=2,relief='solid').place(x=-2,y=-1,width=405,height=50)

            idLb = Label(showUserWin,text=' User ID : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=60,width=150,height=30)
            idLbShow = Label(showUserWin,text=id,font=Font,bg='#E7E7E7',borderwidth=1,relief='solid',anchor='w').place(x=151,y=60,width=50,height=30)
            accessLbShow = Label(showUserWin,text=access,font=Font,bg='#E7E7E7',borderwidth=1,relief='solid').place(x=226,y=60,width=100,height=30)

            usernameLb = Label(showUserWin,text=' ชื่อผู้ใช้ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=95,width=150,height=30)
            usernameLbShow = Label(showUserWin,text=username,font=Font,bg='#E7E7E7',borderwidth=1,relief='solid',anchor='w').place(x=151,y=95,width=200,height=30)

            fnameLb = Label(showUserWin,text=' ชื่อ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=130,width=150,height=30)
            fnameVar = StringVar(showUserWin)
            fnameVar.set(fname)
            fnameEt = Entry(showUserWin,textvariable=fnameVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=130,width=200,height=30)

            lnameLb = Label(showUserWin,text=' นามสกุล : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=165,width=150,height=30)
            lnameVar = StringVar(showUserWin)
            lnameVar.set(lname)
            lnameEt = Entry(showUserWin,textvariable=lnameVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=165,width=200,height=30)

            phoneLb = Label(showUserWin,text=' เบอร์โทรศัพท์ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=200,width=150,height=30)
            phoneVar = StringVar(showUserWin)
            phoneVar.set(phone)
            phoneEt = Entry(showUserWin,textvariable=phoneVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=200,width=200,height=30)

            curPwLb = Label(showUserWin,text=' รหัสผ่านปัจจุบัน : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=235,width=150,height=30)
            currentPasswordVar = StringVar(showUserWin)
            currentPasswordVar.set(password)
            curPwEt = Entry(showUserWin,textvariable=currentPasswordVar,font=Font,bg='white',borderwidth=1,relief='solid').place(x=151,y=235,width=240,height=30)

            accessLb = Label(showUserWin,text=' สิทธิ์ผู้ใช้ : ',font=Font,bg='#D5D5CF',borderwidth=1,relief='groove').place(x=0,y=275,width=150,height=30)
            accessVar = StringVar(showUserWin)
            accessList = ttk.Combobox(showUserWin,font=Font,textvariable=accessVar)
            accessList["values"] = ['MEMBER','STAFF']
            accessVar.set(access)
            accessList.place(x=151,y=275,width=150,height=30)

            def edit():
                newFName = fnameVar.get().capitalize()
                newLName = lnameVar.get().capitalize()
                newPhone = phoneVar.get()
                newPassword = currentPasswordVar.get()
                newAccess = accessVar.get()
                if newFName == fname and newLName == lname and newPhone == phone and newPassword == password and newAccess == access:
                    showUserWin.destroy()
                else:
                    changePwSuccess = None
                    changeDataSuccess = None
                    changeAccess = None
                    if newFName != fname or newLName != lname or newPhone != phone:
                        changeDataSuccess = register.edit(id,newFName,newLName,newPhone)
                    if newPassword != password:
                        changePwSuccess = register.changePassword(id,newPassword)
                    if newAccess != access:
                        changeAccess = register.changeAccess(username,newAccess)
                    if changeDataSuccess != False and changePwSuccess != False and changeAccess != False:
                        showUserWin.destroy()
                    showallusers(empWindow,5,70,590,190)

            editButton = Button(showUserWin,text='แก้ไขข้อมูล',font=("Tahoma Bold", 15),bg='#6AFF55',command=edit).place(x=125,y=425,width=150,height=50)
        
        def cancel():
            updateUserWin.destroy()

        editButton = Button(updateUserWin, text='แสดงข้อมูล',font=("Tahoma",15),bg='#FFF26F',command=editUser,width=10).grid(row=3,column=1)
        cancelBt = Button(updateUserWin,text='กลับ',font=("Tahoma",15),width=10,command=cancel).grid(row=3,column=0)

        updateUserWin.mainloop()

    def updateOrderFunc():
        updateOrderWin = Tk()
        updateOrderWin.title('เลือกรายการสั่งซื้อ')
        updateOrderWin.configure(bg='white')
        updateOrderWin.resizable(False,False)

        idLb = Label(updateOrderWin,text=' Order ID  ',font=("Tahoma",15),bg='white',anchor='e',width=10).grid(row=0,column=0)
        idVar = IntVar(updateOrderWin,value='ระบุ ID')
        idList = ttk.Combobox(updateOrderWin,font=("Tahoma",15),textvariable=idVar)
        idList["values"] = order.allID()
        idList.grid(row=0,column=1)
    
        statusLb = Label(updateOrderWin,text=' สถานะ  ',font=("Tahoma",15),bg='white',anchor='e',width=10).grid(row=1,column=0)
        statusVar = StringVar(updateOrderWin)
        statusVar.set('...')
        statusList = ttk.Combobox(updateOrderWin,font=("Tahoma",15),textvariable=statusVar)
        allStatusList = ['wait','in progress','cancelled','delivered']
        statusList["values"] = allStatusList
        statusList.grid(row=1,column=1)

        def statusUpdate():
            try:
                orderID = idVar.get()
                status = statusVar.get().lower()
                if status in allStatusList:
                    success = order.updateStatus(orderID,status)
                    showallorder(empWindow,5,70,590,190)
                else:
                    tkinter.messagebox.showerror('ERROR','ไม่พบสถานะที่ต้องการอัพเดท')
            except:
                tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด\nOrder ID อาจไม่ถูกต้อง')
    
        def showData():
            try:
                orderID = idVar.get()
                DataWin = Tk()
                DataWin.configure(bg='#E5E5E5')
                DataWin.title('แสดงข้อมูลของ Order ID : {}'.format(orderID))
                status = order.getStatus(orderID)

                personalData(DataWin,orderID)
                productButton(DataWin,orderID,True)

                if status == 'cancelled':
                    Label(DataWin,text='\n\n\tรายการสั่งซื้อนี้ถูกยกเลิกแล้ว',font=("Tahoma",12),width=25,anchor='e',bg='#E5E5E5').grid(row=99,column=0,sticky='E')
                elif status == 'delivered':
                    Label(DataWin,text='\n\n\tรายการนี้ดำเนินการเรียบร้อยแล้ว',font=("Tahoma",12),width=25,anchor='e',bg='#E5E5E5').grid(row=99,column=0,sticky='E')
                DataWin.mainloop
            except:
                tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด\nOrder ID อาจไม่ถูกต้อง')

        def setStatus():
            try:
                orderID = idVar.get()
                if order.check(orderID) == False:
                    statusVar.set('---')
                
                curStatus = order.getStatus(orderID)
                statusVar.set(curStatus)
            
            except:
                tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด')

        def cancel():
            updateOrderWin.destroy()

        editBt = Button(updateOrderWin,text='อัพเดท',font=("Tahoma",15),bg='#86E5EC',width=10,command=statusUpdate).grid(row=3,column=1)
        infoBt = Button(updateOrderWin,text='แสดงข้อมูล',font=("Tahoma",15),bg='#FFF26F',width=10,command=showData).grid(row=3,column=2)
        checkBt = Button(updateOrderWin,text='ตรวจสอบ',font=("Tahoma",15),bg='#FFFFFF',width=10,command=setStatus).grid(row=0,column=2)
        cancelBt = Button(updateOrderWin,text='กลับ',font=("Tahoma",15),bg='#FFB1B1',width=10,command=cancel).grid(row=3,column=0)
    
    def showProductSec():
        clear = Label(empWindow,text='',bg='grey').place(x=-1,y=70,width=650,height=485)
        show(empWindow,5,70,590,190)
        add = Button(empWindow, text='เพิ่มสินค้า',image=plusImage,compound=TOP,font=("Tahoma",15),bg='#A1FF8F',command=addFunc).place(x=50,y=300,width=200,height=150)
        editBt = Button(empWindow, text='แก้ไขสินค้า',image=editIcon,compound=TOP,font=('Tahoma',15),bg='yellow',command=edit).place(x=350,y=300,width=200,height=150)

    def showOrderSec():
        clear = Label(empWindow,text='',bg='grey').place(x=-1,y=70,width=650,height=485)
        showallorder(empWindow,5,70,590,190)
        updateorderstatus = Button(empWindow,text='แสดง/อัพเดทสถานะรายการสั่งซื้อ',image=updateIcon,compound=TOP,font=('Tahoma',15),bg='#3AF0FF',command=updateOrderFunc).place(x=100,y=300,width=400,height=150)

    def showUserSec():
        clear = Label(empWindow,text='',bg='grey').place(x=-1,y=70,width=650,height=485)
        showallusers(empWindow,5,70,590,190)
        editaccessuser = Button(empWindow, text='แก้ไขสมาชิก',image=cardIcon,compound=TOP,font=("Tahoma",15),bg='#FFFD8C',command=updateUser).place(x=175,y=300,width=250,height=150)

    plusImageFile = PhotoImage(file = r"plus.png")
    plusImage = plusImageFile.subsample(7,7)
    editIconFile = PhotoImage(file = r"Edit.png")
    editIcon = editIconFile.subsample(14,14)
    updateIconFile = PhotoImage(file = r"update.png")
    updateIcon = updateIconFile.subsample(5,5)
    cardIconFile = PhotoImage(file = r"acc_card.png")
    cardIcon = cardIconFile.subsample(7,7)
    productSection = Button(empWindow, text='สินค้า',font=("Tahoma Bold",10),bg='white',command=showProductSec).place(x=0,y=0,width=100,height=50)
    orderSection = Button(empWindow, text='รายการสั่งซื้อ',font=("Tahoma Bold",10),bg='white',command=showOrderSec).place(x=150,y=0,width=100,height=50)
    userSection = Button(empWindow, text='สมาชิก',font=("Tahoma Bold",10),bg='white',command=showUserSec).place(x=300,y=0,width=100,height=50)

    showProductSec()

    backImageRaw = PhotoImage(file = r"back.png")
    backImage = backImageRaw.subsample(3,3)

    Button(empWindow, text='BACK', image = backImage, font=("Tahoma",10),command=lambda: back(empWindow)).place(x=1,y=555,width=70,height=70)
     
    go = Menu(empWindow)
    menuItem = Menu(empWindow)
    menuItem.add_command(label='กลับหน้าแรก',font=("Tahoma",10),command=lambda: back(empWindow))
    menuItem.add_command(label='ออกจากโปรแกรม',font=("Tahoma",10),command=lambda: exit(empWindow))
    #Main Menu: GO
    go.add_cascade(label='Go',menu=menuItem)
    empWindow.config(menu=go)

    empWindow.mainloop()

# Function: Create Personal Data Label
def personalData(main, id):
    if order.check(id) == False:
        Label(main,text='* * ไม่พบข้อมูล! * *',font=("Tahoma",15)).grid(row=0,column=0)
    else:
        c.execute('SELECT * FROM userorders WHERE id = ?', (id,))
        username = userLogin
        userData = register.getDataUsername(username) # [0 ID, 1 Username, 2 Password, 3 F Name, 4 L Name, 5 Phone, 6 Access]
        name = userData[3] + ' ' + userData[4]
        phone = userData[5]
        result = c.fetchall()
        r = result[0]
        Label(main,text='รายละเอียดของ Order ID : \n',font=("Tahoma",12),bg='#E5E5E5').grid(row=0,column=0,sticky='E')
        Label(main,text='วันที่สั่ง',font=("Tahoma",12),bg='#E5E5E5').grid(row=1,column=0,sticky='E')
        Label(main,text='ชื่อผู้ใช้',font=("Tahoma",12),bg='#E5E5E5').grid(row=2,column=0,sticky='E')
        Label(main,text='ชื่อ',font=("Tahoma",12),bg='#E5E5E5').grid(row=3,column=0,sticky='E')
        Label(main,text='เบอร์โทรศัพท์',font=("Tahoma",12),bg='#E5E5E5').grid(row=4,column=0,sticky='E')
        Label(main,text='ที่อยู่',font=("Tahoma",12),bg='#E5E5E5').grid(row=5,column=0,sticky='E')
        Label(main,text='สถานะ',font=("Tahoma",12),bg='#E5E5E5').grid(row=7,column=0,sticky='E')

        idLb = Label(main,text='{}\n'.format(r[0]),font=("Tahoma",12),anchor='w',bg='#E5E5E5').grid(row=0,column=1,sticky='W',columnspan=4)
        dateLb = Label(main,text=r[1],font=("Tahoma",12),anchor='w',borderwidth=1,relief="solid",bg='white').grid(row=1,column=1,sticky='W',columnspan=4)
        usernameLb = Label(main,text=username,font=("Tahoma",12),width=40,anchor='w',borderwidth=1,relief="solid",bg='white').grid(row=2,column=1,sticky='W',columnspan=4)
        nameLb = Label(main,text=name,font=("Tahoma",12),width=40,anchor='w',borderwidth=1,relief="solid",bg='white').grid(row=3,column=1,sticky='W',columnspan=4)
        phoneLb = Label(main,text=phone,font=("Tahoma",12),width=40,anchor='w',borderwidth=1,relief="solid",bg='white').grid(row=4,column=1,sticky='W',columnspan=4)
        addressLb = Label(main,text=r[3],font=("Tahoma",12),width=40,anchor='w',borderwidth=1,relief="solid",bg='white').grid(row=5,column=1,sticky='NW',columnspan=4)
        statusLb = Label(main,text=r[5],font=("Tahoma",12),width=10,anchor='w',borderwidth=1,relief="solid",bg='white').grid(row=7,column=1,sticky='W',columnspan=4)

# Function: Create Product List Button
def productButton(main,id,data):
    allProducts = product.getAllProducts()
    allProducts.sort()
    orderList = {}
    global currentPage
    global totalAmount
    global totalPrice
    currentPage = 0
    totalAmount = 0
    totalPrice = 0
    orderStatus = ''
    if order.check(id) == True:
        orderList = order.getOrderListID(id)
        orderStatus = order.getStatus(id)
        for x,y in orderList.items():
            price = product.getPrice_name(x)
            totalAmount += y
            totalPrice += (price * y)
    else:
        orderList = {}
        orderStatus = 'wait'
    if data == True:
        orderStatus = 'x'
    def addItem(i):
        global totalAmount
        global totalPrice
        if allProducts[i] not in orderList:
            orderList[allProducts[i]] = 1
            totalAmount += 1
            totalPrice = totalPrice + (product.getPrice_name(allProducts[i]) * 1)
        else:
            orderList[allProducts[i]] += 1
            totalAmount += 1
            totalPrice = totalPrice + (product.getPrice_name(allProducts[i]) * 1)
        amount = orderList.get(allProducts[i])
        Row = 0
        if currentPage == 0:
            Row = i + 11
        else:
            Row = (i - (currentPage * 10)) + 11
        amountEt = Label(main, text=amount,bg='white',font=("Tahoma",10),width=5).grid(row=Row,column=1)
        AmountPriceLb = Label(main, text='รวม: x{:,} | ฿{:,.2f}'.format(totalAmount, totalPrice),font=("Tahoma", 12),bg='white',width=20).grid(row=10,column=2,columnspan=3)

    def removeItem(i):
        global totalAmount
        global totalPrice
        if allProducts[i] not in orderList:
            orderList[allProducts[i]] = 0
            amount = 0
        else:
            orderList[allProducts[i]] -= 1
            totalAmount -= 1
            totalPrice = totalPrice - (product.getPrice_name(allProducts[i]) * 1)
        amount = orderList.get(allProducts[i])
        if amount == 0:
            orderList.pop(allProducts[i])
        Row = 0
        if currentPage == 0:
            Row = i + 11
        else:
            Row = (i - (currentPage * 10)) + 11
        amountEt = Label(main, text=amount,bg='white',font=("Tahoma",10),width=5).grid(row=Row,column=1)
        AmountPriceLb = Label(main, text='รวม: x{:,} | ฿{:,.2f}'.format(totalAmount, totalPrice),font=("Tahoma", 12),bg='white',width=20).grid(row=10,column=2,columnspan=3)

    def clearItem(i):
        global totalAmount
        global totalPrice
        amount = orderList.get(allProducts[i])
        if allProducts[i] in orderList:
            orderList.pop(allProducts[i])
            totalAmount -= amount
            totalPrice = totalPrice - (product.getPrice_name(allProducts[i]) * amount)
        amount = 0
        Row = 0
        if currentPage == 0:
            Row = i + 11
        else:
            Row = (i - (currentPage * 10)) + 11
        amountEt = Label(main, text=amount,bg='white',font=("Tahoma",10),width=5).grid(row=Row,column=1)
        AmountPriceLb = Label(main, text='รวม: x{:,} | ฿{:,.2f}'.format(totalAmount, totalPrice),font=("Tahoma", 12),bg='white',width=20).grid(row=10,column=2,columnspan=3)

    def nextPage():
        global currentPage
        currentPage += 1
        showItem(currentPage)
        return currentPage

    def previousPage():
        global currentPage
        currentPage -= 1
        showItem(currentPage)
        return currentPage

    def showItem(page):
        global totalAmount
        global totalPrice
        firstItem = 0 + (currentPage * 10)
        finalItem = 10 + (currentPage * 10)
        allPage = 0
        itemInPage = []
        orderItems = []
        if orderStatus != 'wait':
            orderItems = order.getOrderListID_list(id)
            orderItems.sort()
            itemInPage = orderItems[firstItem:finalItem]
            allPage = ((len(orderItems) - 1) // 10) 
        else:
            allPage = ((len(allProducts) - 1) // 10) 
            itemInPage = allProducts[firstItem:finalItem]
        infoLabel = Label(main, text='สินค้า : หน้า {}'.format(page+1),font=('Tahoma Bold',15),bg='#E6E6E6').grid(row=10,column=0)
        amountLabel = Label(main, text='จำนวน',font=('Tahoma',15),bg='#E6E6E6').grid(row=10,column=1)
        for x in range(len(itemInPage)):
            i = x + (page * 10)
            button = Label(main, text='{} (฿{})'.format(itemInPage[x], product.getPrice_name(itemInPage[x])).capitalize(),bg='#FFFFFF',width=25,height=2,font=("Tahoma",10),borderwidth=1,relief='groove').grid(row=x+11, column=0,sticky=W)
            if orderStatus == 'wait':
                if allProducts[i] in orderList:
                    amount = orderList.get(allProducts[i])
                else:
                    amount = 0
            else:
                amount = orderList.get(orderItems[i])
            AmountPriceLb = Label(main, text='รวม: x{:,} | ฿{:,.2f}'.format(totalAmount, totalPrice),font=("Tahoma", 12),bg='white',width=20).grid(row=10,column=2,columnspan=3)
            amountEt = Label(main, text=amount,bg='white',font=("Tahoma",10),width=5).grid(row=x+11,column=1)
            if orderStatus == 'wait':
                removeButton = Button(main, text='-',bg='#FFFFFF',fg='red', command=lambda a=i: removeItem(a),font=("Tahoma Bold",8),width=2).grid(row=x+11,column=1,sticky=W)
                addButton = Button(main, text='+',bg='#FFFFFF',fg='green', command=lambda a=i: addItem(a),font=("Tahoma Bold",8),width=2).grid(row=x+11,column=1,sticky=E)
                clearButton = Button(main, text='ลบ',bg='#FFFFFF', command=lambda a=i: clearItem(a),font=("Tahoma",8),width=6).grid(row=x+11,column=2)
            else:
                Label(main, text='',bg='#E5E5E5',width=2).grid(row=x+11,column=1,sticky=W)
                Label(main, text='',bg='#E5E5E5',width=2).grid(row=x+11,column=1,sticky=E)
                Label(main, text='',bg='#E5E5E5',width=6).grid(row=x+11,column=2)

        if currentPage > 0:
            previousPageButton = Button(main,text='หน้า {}'.format((currentPage + 1)-1),fg='red',width=10,height=1,command=previousPage,font=("Tahoma",10)).grid(row=99,column=0)  
        else:
            previousPageButton = Label(main,text='',bg='#E5E5E5',width=12,height=2,font=("Tahoma",10)).grid(row=99,column=0)  
        if currentPage != allPage and allPage > 0:
            nextPageButton = Button(main,text='หน้า {}'.format((currentPage + 1)+1),fg='green',width=10,height=1,command=nextPage,font=("Tahoma",10)).grid(row=99,column=2,columnspan=2,sticky=W)
        else:
            nextPageButton = Label(main,text='',bg='#E5E5E5',width=12,height=2,font=("Tahoma",10)).grid(row=99,column=2,columnspan=2,sticky=W)
        if len(itemInPage) < 10:
            empty = 10 - len(itemInPage)
            for z in range(empty):
                button = Label(main, text='',bg='#E5E5E5',width=25,height=2).grid(row=z+(21-empty), column=0,sticky=W)
                removeButton = Label(main, text='',bg='#E5E5E5', width=3,height=2).grid(row=z+(21-empty),column=1,sticky=W)
                amountEt = Label(main, text='',bg='#E5E5E5', width=5,height=2).grid(row=z+(21-empty),column=1)
                addButton = Label(main, text='',bg='#E5E5E5', width=3,height=2).grid(row=z+(21-empty),column=1,sticky=E)
                clearButton = Label(main, text='',bg='#E5E5E5',width=7,height=2).grid(row=z+(21-empty),column=2)
    showItem(currentPage)
    return orderList

def Customer():
    ctWindow = Tk()
    ctWindow.title('สั่งสินค้า')
    ctWindow.geometry('600x600')
    ctWindow.configure(bg='grey')
    ctWindow.resizable(False,False)

    username = userLogin
    userData = register.getDataUsername(username) # [0 ID, 1 Username, 2 Password, 3 F Name, 4 L Name, 5 Phone, 6 Access]
    name = userData[3] + ' ' + userData[4]
    phone = userData[5]

    #
    def addFunc():
        addOrder = Tk()
        addOrder.title('สั่งซื้อสินค้า')
        addOrder.configure(bg='#E5E5E5')
        addOrder.resizable(False,False)
        
        Label(addOrder,text='ชื่อของคุณ (ภาษาอังกฤษ)',font=("Tahoma",12),bg='#E5E5E5',borderwidth=1,relief='ridge',width=20,anchor='e').grid(row=0,column=0,sticky='E')
        Label(addOrder,text='เบอร์โทรศัพท์',font=("Tahoma",12),bg='#E5E5E5',borderwidth=1,relief='ridge',width=20,anchor='e').grid(row=1,column=0,sticky='E')
        Label(addOrder,text='ที่อยู่',font=("Tahoma",12),bg='#E5E5E5',borderwidth=1,relief='ridge',width=20,anchor='e').grid(row=2,column=0,sticky='E')

        nameEnt = Label(addOrder,font=("Tahoma",12),text=name,width=55,anchor='w',borderwidth=1,relief='groove',bg='white').grid(row=0,column=1,sticky='W',columnspan=4)
        phoneEnt = Label(addOrder,font=("Tahoma",12),text=phone,width=55,anchor='w',borderwidth=1,relief='groove',bg='white').grid(row=1,column=1,sticky='W',columnspan=4)
        customerAddress = StringVar(addOrder)
        addressEnt = Entry(addOrder,font=("Tahoma",12),textvariable=customerAddress,width=55).grid(row=2,column=1,sticky='NW',columnspan=4)

        orderList = productButton(addOrder,0,False)

        def add():
            try:
                dateNow = datetime.datetime.now()
                date = dateNow.strftime("%Y-%m-%d-%H:%M:%S")
                address = customerAddress.get()

                success = order.add(date,username,address,orderList)
                if success == True:
                    addOrder.destroy()
            except:
                tkinter.messagebox.showerror('ERROR', 'พบข้อผิดพลาด')

        def cancelCmd():
            addOrder.destroy()

        add = Button(addOrder,text='สั่งสินค้า',font=("Tahoma",15),command=add,width=10,bg='#22E800').grid(row=5,column=2,columnspan=2)
        cancelBt = Button(addOrder,text='ยกเลิก',font=("Tahoma",15),command=cancelCmd,width=10,bg='#FF9898').grid(row=5,column=0,columnspan=2)

        addOrder.mainloop()
    
    def editSelection():
        editSelectOrder = Tk()
        editSelectOrder.title('เลือก Order ที่ต้องการแก้ไขของ {}'.format(username))
        editSelectOrder.resizable(False,False)

        def openEdit(id):
            orderList = order.getOrderListID(id)
            status = order.getStatus(id)
            editOrderWin = Tk()            
            editOrderWin.title('แก้ไขรายการสั่งซื้อ')
            editOrderWin.configure(bg='#E5E5E5')
            editOrderWin.resizable(False,False)
                        
            personalData(editOrderWin,id)

            allProducts = product.getAllProducts()
            orderList = productButton(editOrderWin,id,False)
                
            def editOrder():
                try:
                    success = order.edit(id,orderList)
                    if success == True:
                        editOrderWin.destroy()
                        editSelectOrder.destroy()
                        editSelection()
                except:
                    tkinter.messagebox.showerror('ERROR', 'พบข้อผิดพลาด')
            
            def cancelOrder():
                success = order.cancel(id)
                if success == True:
                    editOrderWin.destroy()
                    editSelectOrder.destroy()
                    editSelection()

            if status == 'wait':
                editButton = Button(editOrderWin,text='แก้ไขรายการ',font=("Tahoma",15),command=editOrder,width=12,bg='#94FF35').grid(row=8,column=2,columnspan=2)
                cancelButton = Button(editOrderWin,text='ยกเลิกรายการ',font=("Tahoma",15),command=cancelOrder,width=12,bg='#FF8888').grid(row=8,column=0,columnspan=2)
            else:
                editButton = Label(editOrderWin,bg='#E5E5E5',width=12).grid(row=8,column=2,columnspan=2)


        c.execute('SELECT * FROM userorders WHERE username = ?', (username,))
        result = c.fetchall()
        if len(result) == 0:
            Label(editSelectOrder,text='\n" ไม่พบรายการสั่งซื้อ "\n',font=("Tahoma",15),width=50).grid(row=0,column=0)
        for i in range(len(result)):
            r = result[i]
            header = Label(editSelectOrder,text='ID',font=("Tahoma",12),width=5).grid(row=0,column=0)
            header = Label(editSelectOrder,text='Date',font=("Tahoma",12),width=30).grid(row=0,column=1)
            header = Label(editSelectOrder,text='Status',font=("Tahoma",12),width=10).grid(row=0,column=4)
            DateLb = Label(editSelectOrder,text=r[1],font=("Tahoma",12),width=30).grid(row=i+1,column=1)
            statusLb = Label(editSelectOrder,text=r[5],font=("Tahoma",12),width=10).grid(row=i+1,column=4)
            idLb = Label(editSelectOrder,text=r[0],font=("Tahoma",12),bg='white',width=5,borderwidth=2,relief='groove',height=2).grid(row=i+1,column=0)
            show = Button(editSelectOrder,text='แสดง/แก้ไข',font=('Tahoma',12),width=10,command=lambda x=r[0]: openEdit(x),bg='#F3FF00').grid(row=i+1,column=6)

    def receipt():
        preReceiptWin = Tk()
        preReceiptWin.title('The Boss Delivery Receipt')
        preReceiptWin.resizable(False,False)

        idLb = Label(preReceiptWin,text='ID  ',font=("Tahoma",15),anchor='e',width=10).grid(row=0,column=0)
        idVar = IntVar(preReceiptWin,value='ระบุ ID')
        idList = ttk.Combobox(preReceiptWin,font=("Tahoma",15),textvariable=idVar)
        idList["values"] = order.userListID(username)
        idList.grid(row=0,column=1)

        def showReceipt():
            try:
                id = idVar.get()
                if order.check(id) == False:
                    tkinter.messagebox.showwarning('ERROR','ไม่พบ Order ID ที่ต้องการ')
                else:
                    IDCheck = order.userListID(userLogin)
                    if id not in IDCheck:
                        tkinter.messagebox.showwarning('ERROR','ไม่พบ Order ID ของคุณ\n(คุณสามารถตรวจสอบได้เฉพาะรายการของคุณ)')
                    else:
                        preReceiptWin.destroy()
                        receiptWin = Tk()
                        receiptWin.title('The Boss Deliery Receipt')
                        receiptWin.configure(bg='white')
                        receiptWin.resizable(False,False)
                        calc = order.calculate(id)
                        username = order.getName(id)
                        name = register.getName(username)
                        orderList = order.getOrderListID(id)
                        distancePrice = 10
                        address = order.getAddress(id)
                        phone = register.getPhone(username)
                        date = order.getDate(id)
                        status = order.getStatus(id)
                        theFont = ("Tahoma",12)
                        w = 50
                        Info = Label(receiptWin,text='-'*85 + '\n' + 'The Boss Delivery'.center(85) + '\n' + 'Receipt'.center(85) + '\n' + '-'*85,font=theFont,anchor='w',bg='white',width=w).grid(row=0,column=0)
                        line1 = Label(receiptWin,text='\nOrder ID : {}'.format(id),font=theFont,anchor='w',bg='white',width=w).grid(row=1,column=0)
                        line2 = Label(receiptWin,text='Date : {}'.format(date),font=theFont,anchor='w',bg='white',width=w).grid(row=2,column=0)
                        line3 = Label(receiptWin,text='Customer Name : {}'.format(name),font=theFont,anchor='w',bg='white',width=w).grid(row=3,column=0)
                        line4 = Label(receiptWin,text='Phone Number : {}'.format(phone),font=theFont,anchor='w',bg='white',width=w).grid(row=4,column=0)
                        line4 = Label(receiptWin,text='\nOrder List : ',font=theFont,anchor='w',bg='white',width=w).grid(row=5,column=0)
                        line_head = Label(receiptWin,text='{} \t {} '.format('', 'Item'),font=theFont,anchor='w',bg='white',width=w).grid(row=6,column=0)
                        line_headprice = Label(receiptWin,text='{}'.format('Price'),font=theFont,anchor='w',bg='white',width=10).grid(row=6,column=0,sticky='E')
                        for i in range(len(orderList)):
                            keys = list(orderList.keys())
                            x = keys[i]
                            productPrice = product.getPrice_name(x)
                            y = orderList.get(x)
                            line_order = Label(receiptWin,text='x{} \t {} '.format(y, x),font=theFont,anchor='w',bg='white',width=w).grid(row=i+7,column=0)
                            column_price = Label(receiptWin,text='฿{:,.2f}'.format((y*productPrice)),font=theFont,anchor='w',bg='white',width=10).grid(row=i+7,column=0,sticky='E')
                        
                        line_delivery = Label(receiptWin,text='{}'.format('Delivery Cost'),font=theFont,anchor='w',bg='white',width=w).grid(row=len(orderList)+10,column=0)
                        line_delivery_price = Label(receiptWin,text='฿{:,.2f}'.format(distancePrice),font=theFont,anchor='w',bg='white',width=10).grid(row=len(orderList)+10,column=0,sticky='E')
                        total = Label(receiptWin,text='\nTotal : ฿{:,.2f}'.format(calc),font=theFont,anchor='w',bg='white',width=20).grid(row=len(orderList)+11,column=0,sticky='W')
                        if status == 'cancelled':
                            statusLine = Label(receiptWin,text='\nรายการสั่งซื้อนี้ถูกยกเลิกแล้ว',font=theFont,bg='white').grid(row=len(orderList)+98,column=0)
                        line_final = Label(receiptWin,text='\n' + '_'*85,font=theFont,anchor='w',bg='white',width=w).grid(row=len(orderList)+99,column=0)
            except:
                tkinter.messagebox.showerror('ERROR','พบข้อผิดพลาด')


        go = Button(preReceiptWin,text='แสดงผล',font=("Tahoma",15),command=showReceipt).grid(row=1,column=1)

    plusImageFile = PhotoImage(file = r"plus.png")
    plusImage = plusImageFile.subsample(4,4)
    docsImageFile = PhotoImage(file = r"docs.png")
    docsImage = docsImageFile.subsample(4,4)
    receiptImageFile = PhotoImage(file = r"receipt.png")
    receiptImage = receiptImageFile.subsample(4,4)

    infoLabel = Label(ctWindow,text="เลือกรายการที่ต้องการดำเนินการ",font=('Tahoma',25),bg='#FFFFFF',borderwidth=1,relief='ridge').place(x=0,y=0,width=600)
    addButton = Button(ctWindow,text="สั่งสินค้า",font=('Tahoma',20),image=plusImage,compound=TOP,command=addFunc,bg='#A1FF8F').place(x=50,y=100,width=200,height=200)
    editButton = Button(ctWindow,text="แสดงรายการสั่งซื้อ",font=('Tahoma',15),image=docsImage,compound=TOP,command=editSelection,bg='#c9e3fc').place(x=350,y=100,width=200,height=200)
    receiptButton = Button(ctWindow,text="ใบเสร็จ",font=('Tahoma',15),image=receiptImage,compound=TOP,command=receipt,bg='#FFFFFF').place(x=200,y=350,width=200,height=200)

    backImageRaw = PhotoImage(file = r"back.png")
    backImage = backImageRaw.subsample(3,3)

    Button(ctWindow, text='BACK', image = backImage, font=("Tahoma",10),command=lambda: back(ctWindow)).place(x=1,y=530,width=70,height=70)

    go = Menu(ctWindow)
    menuItem = Menu(ctWindow)
    menuItem.add_command(label='กลับหน้าแรก',font=("Tahoma",10),command=lambda: back(ctWindow))
    menuItem.add_command(label='ออกจากโปรแกรม',font=("Tahoma",10),command=lambda: exit(ctWindow))
    #Main Menu: GO
    go.add_cascade(label='Go',menu=menuItem)
    ctWindow.config(menu=go)

    ctWindow.mainloop()

createDatabaseTable()
createAdmin()
Main()