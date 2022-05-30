# Homework
# Create Tab in tkinter that we called "Notebook"
# Insert background picture that we use "PhotoImage" function
# Insert icon image at Tab and Button

from tkinter import * # * will import only main file (__init__.py) excluded sub files (ttk and others)
from tkinter import ttk, messagebox
from datetime import datetime
import csv

# strftime is string format time

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

today = datetime.now().strftime('%a') # %a is day such as Mon, Tue and etc.
dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # year-month-date hour-minute-second
dt = days[today]+'-'+dt # today will be changed as the current day

GUI = Tk()
GUI.title('Expense recording program by SS')
GUI.geometry('700x800+1000+100')

############## MENU ##################
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0) # tearoff=0 is commade to delete ---------- of the commande in menu
menubar.add_cascade(label='File',menu=filemenu) # .add_cascade is bring object to menu
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
# Help menu
def About():
    messagebox.showinfo('About','Hello, this is program to record information\nIf you interested this program, please send the BTC to\nAddress : AAA')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About) #command=About is link the def About():
# Donate menu
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)


################################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1) # fill=BOTH is expanding for X and Y axis # 1 is true
expense_icon = PhotoImage(file='AddExpense.png') # .subsample(2) = abbreviate picture size to 2 times
list_icon = PhotoImage(file='ListExpense.png')
Tab.add(T1,text=f'{"Add Expense":^{30}}',image=expense_icon,compound='left') 
Tab.add(T2,text=f'{"List Expense":^{30}}',image=list_icon,compound='left') 

F1 = Frame(T1)
# F1.place(x=100,y=50)
F1.pack()

FONT1 = (None,20)

Background = PhotoImage(file='Background.png')
Mainicon = Label(F1,image=Background)
Mainicon.pack()

L1 = ttk.Label(F1,text='Expense Name',font=FONT1).pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack() # to use E1.focus()

L2 = ttk.Label(F1,text='Price',font=FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1).pack()
# E2.pack()

L3 = ttk.Label(F1,text='Quantity',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1).pack()
# E3.pack()

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('ERROR','Please insert Expense information.')
        return
    elif price =='':
        messagebox.showwarning('ERROR','Please insert Price information.')
        return
    elif quantity =='':
        quantity = 1 # if quantity is none, we will fix minimum quantity = 1
        # messagebox.showwarning('ERROR','Please insert Quantity information.')
        # return

    try:
        total = float(price)*float(quantity)

        print('Expense : {}, Price : {}, Quantity : {}, Total : {}'.format(expense,price,quantity,total))
        resulttext = 'Expense : {}, Price : {} Baht,\n'.format(expense,price)
        resulttext = resulttext + 'Quantity : {} pc, Total : {} Baht'.format(quantity,total)
        v_result.set(resulttext)

        v_expense.set('') # clear old data for reset to receive the new data
        v_price.set('')
        v_quantity.set('')

        with open('EP6 treeview.csv','a',encoding='utf-8',newline='') as f:
            fw = csv.writer(f)
            data = [dt,expense,price,quantity,total]
            fw.writerow(data)
        E1.focus()
        update_table()
    except Exception as e:
        print('ERROR',e)
        print('ERROR')
        # messagebox.showerror('ERROR','Please insert information again, wrong information type.')
        messagebox.showwarning('ERROR','Please insert information again, wrong information type.')
        # messagebox.showinfo('ERROR','Please insert information again, wrong information type.')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')
        E1.focus()



Save_icon = PhotoImage(file='SaveButton.png')
B1 = ttk.Button(F1,text=f'{"Save":>{15}}',image=Save_icon,compound='left',command=Save) # .pack() # normal button size
B1.pack(ipadx=50,ipady=20,pady=20) # pady is create free space in Y axis from the upper data

v_result = StringVar()
v_result.set('-------Result-------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='green') # foreground is color
result.pack(pady=20)

############ TAB 2 ##############

def read_csv():
    with open('EP6 treeview.csv',newline='',encoding='utf-8') as f: # as f is name
        fr = csv.reader(f)
        data = list(fr)
    return data

# table
L = ttk.Label(T2,text='Result table',font=FONT1).pack(pady=20)

header = ['Date-Time','Expense','Price','Quantity','Total']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10) # show='headings' is for can not show sub items # height = row quantity
resulttable.pack()

'''
for i in range(len(header)):
    resulttable.heading(header[i],text=header[i])
'''

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,80]
for h,w in zip(header,headerwidth): # zip is command for pair the header and headerwidth together
    resulttable.column(h,width=w)

'''
# insert parameter in table by manual
resulttable.insert('',0,value=['Monday','water',30,5,150]) # fix '' # 0 is index 0 or row 0
resulttable.insert('','end',value=['Tuesday','water',30,5,150]) # fix '' # 'end' is last row
'''

def update_table():
    resulttable.delete(*resulttable.get_children()) # * is for loop # this function to clear old data
    # for c in resulttable.get_children():
        # resulttable.delete(c)
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()
print('GET CHILD:',resulttable.get_children())

GUI.bind('<Return>',Save)
GUI.mainloop()
