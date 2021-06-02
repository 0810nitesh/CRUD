from tkinter import Tk, Scrollbar, Button,Label, Listbox,StringVar,Entry ,W,E,N,S, END
from tkinter import ttk
from tkinter import messagebox
import psycopg2 as psy
from db import dbcon

con=psy.connect(**dbcon)
print(con)

cursor=con.cursor() 

class todoapp():
	def __init__(self):
		self.con=psy.connect(**dbcon)
		self.cursor=con.cursor() 
		print(f"You have connected to database")
	
	def __del__(self):
		self.con.close()

	def view(self):
		self.cursor.execute("SELECT * from todo")
		rows=self.cursor.fetchall()
		return rows

	def insert(self,title):
		sql=("INSERT INTO todo(title) VALUES (%s)")
		values=[title]
		self.cursor.execute(sql,values)
		self.con.commit()
		messagebox.showinfo(title="TodoList Database", message="New task added")

	def update(self,id,title):
		tsql='UPDATE  todo SET title=%s WHERE id=%s'
		self.cursor.execute(tsql,[title,id])
		self.con.commit()
		messagebox.showinfo(title="TodoList Database", message="Task Updated")	

	def delete(self,id):
		delete ='DELETE FROM todo WHERE id=%s'
		self.cursor.execute(delete,[id])
		self.con.commit()
		messagebox.showinfo(title="TodoList Database", message="Task Deleted")	

db= todoapp()

def get_selected_row(event):
	global selected_task
	index=list_box.curselection()[0]
	selected_task=list_box.get(index)
	title_entry.delete(0,'end')
	title_entry.insert('end',selected_task[1])

def view_records():
	list_box.delete(0,'end')
	for row in db.view():
		list_box.insert('end',row)



def add_book():
	db.insert(title_text.get())
	list_box.delete(0,'end')
	list_box.insert('end',(title_text.get()))
	title_entry.delete(0,'end')
	con.commit()
	view_records()
	clear_screen()

def delete_records():
	db.delete(selected_task[0])
	con.commit()
	view_records()
	clear_screen()

def clear_screen():
	title_entry.delete(0,'end')

def update_records():
	db.update(selected_task[0],title_text.get())
	title_entry.delete(0,'end')
	con.commit()
	view_records()
	clear_screen()



root=Tk()

root.title("CRUD")
root.configure(background="light green")
root.geometry("550x500")

title_label=ttk.Label(root,text="Task",background="light green", font=("TkDefaultFont",15))
title_label.grid(row=0,column=0,sticky=W)

title_text= StringVar()

title_entry=ttk.Entry(root,width=25,textvariable=title_text)
title_entry.grid(row=0,column=1,sticky=W)

add_btn=Button(root,text="Add Task", bg="blue",fg="white", font="TkDefaultFont 10 bold" ,command=add_book)
add_btn.grid(row=0,column=2,sticky=W)

list_box=Listbox(root,height=16 ,width= 40,font="TkDefaultFont, 13", bg="light blue")
list_box.grid(row=3,column=1,columnspan=14, sticky= W+E,pady=40,padx=15)
list_box.bind('<<ListboxSelect>>',get_selected_row)

scroll_bar=Scrollbar(root)
scroll_bar.grid(row=1,column=14,rowspan=14,sticky=W)

list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)

modify_btn=Button(root,text="Modify",bg="orange",fg="white",font="TkDefaultFont 10 bold", command=update_records)
modify_btn.grid(row=15,column=1)

delete_btn=Button(root,text="Delete",bg="purple",fg="white",font="TkDefaultFont 10 bold", command=delete_records)
delete_btn.grid(row=15,column=2, padx=35)

exit_btn=Button(root,text="Exit",bg="red",fg="white",font="TkDefaultFont 10 bold", command=root.destroy)
exit_btn.grid(row=15,column=3)

view_records()

root.mainloop()