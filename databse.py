from tkinter import *
import sqlite3

root = Tk()
root.title('Debt Tracker')
root.geometry("600x600")

conn = sqlite3.connect('address_book.db')

c = conn.cursor()
'''
c.execute("""CREATE TABLE debt (
        name text,
        casee text,
        total integer,
        amtpaid integer,
        comments text
        )""")
'''
def update():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE debt SET
        name = :name,
        casee = :casee,
        total = :total,
        amtpaid = :amtpaid,
        comments = :comments
        
        WHERE oid = :oid """,
        {
        'name': name_edit.get(),
        'casee': case_edit.get(),
        'total': total_edit.get(),
         'amtpaid': amtpaid_edit.get(),
         'comments': comments_edit.get(),

         'oid': record_id


         })

    conn.commit()

    conn.close()

    name.delete(0, END)
    case.delete(0, END)
    total.delete(0, END)
    amtpaid.delete(0, END)
    comments.delete(0, END)



def edit():
    editor = Tk()
    editor.title('Edit a Record')
    editor.geometry("400x400")

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = delete_box.get()
    #Query database
    c.execute("SELECT * FROM debt WHERE oid = " + record_id)
    records = c.fetchall()


    global name_edit
    global case_edit
    global total_edit
    global amtpaid_edit
    global comments_edit
    # CREATE TEXT BOXES
    name_edit = Entry(editor, width=30)
    name_edit.grid(row=0, column=1, padx=20, pady=(10, 0))
    case_edit = Entry(editor, width=30)
    case_edit.grid(row=1, column=1)
    total_edit = Entry(editor, width=30)
    total_edit.grid(row=2, column=1)
    amtpaid_edit = Entry(editor, width=30)
    amtpaid_edit.grid(row=3, column=1)
    comments_edit = Entry(editor, width=30)
    comments_edit.grid(row=4, column=1)


    # text box labels
    name_label = Label(editor, text="Name")
    name_label.grid(row=0, column=0, pady=(10, 0))
    case_label = Label(editor, text="Case")
    case_label.grid(row=1, column=0)
    total_label = Label(editor, text="Total Owed")
    total_label.grid(row=2, column=0)
    amtpaid_label = Label(editor, text="Payment")
    amtpaid_label.grid(row=3, column=0)
    comments_label = Label(editor, text="Comments")
    comments_label.grid(row=4, column=0)


    for record in records:
        name_edit.insert(0, record[0])
        case_edit.insert(0, record[1])
        total_edit.insert(0, record[2])
        amtpaid_edit.insert(0, record[3])
        comments_edit.insert(0, record[4])
        #balance_edit.insert(0, record[5])

    #Create a save button to save edited record
    edit_btn = Button(editor, text="Save Record", command=update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

# Create function to delete a record
def delete():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE from debt WHERE oid= " + delete_box.get())

    delete_box.delete(0, END)

    conn.commit()

    conn.close()
#create submit function for database
def submit():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()


    c.execute("INSERT INTO debt VALUES (:name, :case, :total, :amtpaid, :comments)",
              {
                  'name': name.get(),
                  'case': case.get(),
                  'total': total.get(),
                  'amtpaid': amtpaid.get(),
                  'comments': comments.get()
              })

    conn.commit()

    conn.close()

    name.delete(0, END)
    case.delete(0, END)
    total.delete(0, END)
    amtpaid.delete(0, END)
    comments.delete(0, END)


#create query function
def query():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM debt")
    records = c.fetchall()
    #print(records)
    print_records = ''
    for record in records:
        y = list(record)
        x = y[2]- y[3]
        #print_records += str(record[0]) + "-" + str(record[1]) +" \t Acc: " +str(record[2])+" Paid: "+ str(record[3])+ " Due: " + str(x)+ " \t \tNotes: " +str(record[4])+  " ID: " + str(record[5])+ "\n"
        print_records += "{0} - {1:20} Acc: {2} Paid: {3} Due: {4:20} Notes: {5} ID: {6} \n".format(str(record[0]),str(record[1]),str(record[2]), str(record[3]), str(x), str(record[4]), str(record[5]))

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)

    conn.commit()

    conn.close()
#CREATE TEXT BOXES
name = Entry(root, width=30)
name.grid(row=0, column=1, padx=20, pady=(10,0))

case = Entry(root, width=30)
case.grid(row=1, column=1)

total = Entry(root, width=30)
total.grid(row=2, column=1)

amtpaid = Entry(root, width=30)
amtpaid.grid(row=3, column=1)

comments = Entry(root, width=30)
comments.grid(row=4, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

#text box labels
name_label = Label(root, text="Name")
name_label.grid(row=0, column=0, pady=(10,0))

case_label = Label(root, text="Case")
case_label.grid(row=1, column=0)

total_label = Label(root, text="Total Owed")
total_label.grid(row=2, column=0)

amtpaid_label = Label(root, text="Payment")
amtpaid_label.grid(row=3, column=0)

comments_label = Label(root, text="Comments")
comments_label.grid(row=4, column=0)

delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=9, column=0, pady=5)

#create a submit button
submit_btn = Button(root, text="Add Record to Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Querey Button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

#Create a Delete Button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

#crate update button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

conn.commit()

conn.close()

root.mainloop()

