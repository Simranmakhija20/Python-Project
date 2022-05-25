from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
import requests
import bs4

mw = Tk()
mw.title("E.M.S")
mw.geometry("850x550+150+80")
mw.configure(bg="lavenderblush")

def f1():
	mw.withdraw()
	aw.deiconify()

def f4():
	mw.withdraw()
	vw.deiconify()
	vw_txt_data.delete(1.0, END)
	con = None
	info = ""
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select * from ems"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "ID : " + str(d[0]) + " Name : " + d[1] + " Salary : " + str(d[2]) + "\n" + "***********************************" + "\n"
		vw_txt_data.insert(INSERT, info)
	except Exception as e:
		showerror("Mistake", e)
	finally:
		if con is not None:
			con.close()

def f6():
	mw.withdraw()
	uw.deiconify()

def f9():
	mw.withdraw()
	dw.deiconify()

def f12():
	con = None
	id = []
	name = []
	salary = []
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select * from ems order by salary desc limit 5"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			id.append(d[0])
			name.append(d[1])
			salary.append(d[2])
		plt.bar(name, salary, width=0.3, color="green")
		plt.xlabel("Employee ID")
		plt.ylabel("Employee Salary")
		plt.title("Top 5 Paid Employee's")
		plt.show()
	except Exception as e :
		showerror("Mistake", e)
	finally:
		if con is not None:
			con.close()


f = ("Times New Roman", 20, "bold")
btn_add = Button(mw, text="Add", font=f, width=12, command=f1)
btn_view = Button(mw, text="View", font=f, width=12, command=f4)
btn_update = Button(mw, text="Update", font=f, width=12, command=f6)
btn_delete = Button(mw, text="Delete", font=f, width=12, command=f9)
btn_charts = Button(mw, text="Charts", font=f, width=12, command=f12)
txt_quote = ScrolledText(mw, font=f, width=50, height=2)

try:
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)

	data = bs4.BeautifulSoup(res.text, "html.parser")
	
	info = data.find("img", {"class":"p-qotd"})

	quote = info["alt"]
	#print(quote)

	txt_quote.insert(INSERT, quote)

except Exception as e:
	showerror("Mistake", e)

y = 10
btn_add.pack(pady=y)
btn_view.pack(pady=y)
btn_update.pack(pady=y)
btn_delete.pack(pady=y)
btn_charts.pack(pady=y)
txt_quote.pack(pady=y)

def f2():
	try:
		id = int(aw_ent_id.get())
		if id<1:
			raise Exception
		else:
			try:
				name = aw_ent_name.get()
				if len(name)<2 or name.isdigit():
					raise Exception
				else:
					try:
						salary = float(aw_ent_salary.get())
						if salary < 8000:
							raise Exception
						else:
							con = None
							try:
								con = connect("ems.db")
								cursor = con.cursor()
								sql = "insert into ems values('%d', '%s', '%f')"
								cursor.execute(sql % (id, name, salary))
								con.commit()
								showinfo("Success", "Record Added Successfully")
								aw_ent_id.delete(0, END)
								aw_ent_name.delete(0, END)
								aw_ent_salary.delete(0, END)
							except Exception as e:
								showerror("Mistake", "ID already exists")
							finally:
								if con is not None:
									con.close()
					except Exception as e:
						showerror("Mistake", "Invalid Salary")
			except Exception as e:
				showerror("Mistake", "Invalid Name")
			
	except Exception as e:
		showerror("Mistake", "Invalid ID")



def f3():
	aw.withdraw()
	mw.deiconify()


aw = Toplevel(mw)
aw.title("Add Emp")
aw.geometry("500x500+300+150")
aw.configure(bg="sky blue")

aw_lbl_id = Label(aw, text="Enter ID", font=f)
aw_ent_id = Entry(aw, font=f, bd=2)
aw_lbl_name = Label(aw, text="Enter Name", font=f)
aw_ent_name = Entry(aw, font=f, bd=2)
aw_lbl_salary = Label(aw, text="Enter Salary", font=f)
aw_ent_salary = Entry(aw, font=f, bd=2)
aw_btn_save = Button(aw, text="Save", font=f, bd=2, width=12, command=f2)
aw_btn_back = Button(aw, text="Back", font=f, bd=2, width=12, command=f3)

aw_lbl_id.pack(pady=y)
aw_ent_id.pack(pady=y)
aw_lbl_name.pack(pady=y)
aw_ent_name.pack(pady=y)
aw_lbl_salary.pack(pady=y)
aw_ent_salary.pack(pady=y)
aw_btn_save.pack(pady=y)
aw_btn_back.pack(pady=y)


aw.withdraw()

def f5():
	vw.withdraw()
	mw.deiconify()

vw = Toplevel(mw)
vw.title("View Emp")
vw.geometry("600x500+220+100")
vw.configure(bg="light yellow")

vw_txt_data = ScrolledText(vw, width=35, height=10, font=f)
vw_btn_back = Button(vw, text="Back", font=f, bd=2, command=f5, width=12)

vw_txt_data.pack(pady=y)
vw_btn_back.pack(pady=y)

vw.withdraw()


def f7():
	con = None
	try:
		id = int(uw_ent_id.get())
		if id < 1:
			raise Exception
		else:
			try:
				name = uw_ent_name.get()
				if len(name)<2 or name.isdigit():
					raise Exception
				else:
					try:
						salary = float(uw_ent_salary.get())
						if salary < 8000:
							raise Exception
						else:
							try:
								con = connect("ems.db")
								cursor = con.cursor()
								sql = "update ems set name = '%s', salary = '%f' where id = '%d'"
								cursor.execute(sql % (name, salary, id))
								if cursor.rowcount==1:
									con.commit()
									showinfo("Success", "Record Updated")
									uw_ent_id.delete(0, END)
									uw_ent_name.delete(0, END)
									uw_ent_salary.delete(0, END)
								else:
									con.rollback()
									showwarning("Absence", "Record does not exists")
									uw_ent_id.delete(0, END)
									uw_ent_name.delete(0, END)
									uw_ent_salary.delete(0, END)
							except Exception as e:
								con.rollback()
								showerror("Mistake", e)
							finally:
								if con is not None:
									con.close()
					except Exception as e:
						showerror("Mistake", "Invalid Salary")
		
			except Exception as e:
				showerror("Mistake", "Invalid Name")
	
	except Exception as e:
		showerror("Mistake", "Invalid ID")

def f8():
	uw.withdraw()
	mw.deiconify()

uw = Toplevel(mw)
uw.title("Update Emp")
uw.geometry("500x500+300+150")
uw.configure(bg="lavender")

uw_lbl_id = Label(uw, text="Enter ID", font=f)
uw_ent_id = Entry(uw, font=f, bd=2)
uw_lbl_name = Label(uw, text="Enter Name", font=f)
uw_ent_name = Entry(uw, font=f, bd=2)
uw_lbl_salary = Label(uw, text="Enter Salary", font=f)
uw_ent_salary = Entry(uw, font=f, bd=2)
uw_btn_save = Button(uw, text="Save", font=f, bd=2, width=12, command=f7)
uw_btn_back = Button(uw, text="Back", font=f, bd=2, width=12, command=f8)

uw_lbl_id.pack(pady=y)
uw_ent_id.pack(pady=y)
uw_lbl_name.pack(pady=y)
uw_ent_name.pack(pady=y)
uw_lbl_salary.pack(pady=y)
uw_ent_salary.pack(pady=y)
uw_btn_save.pack(pady=y)
uw_btn_back.pack(pady=y)


uw.withdraw()


def f10():
	con = None
	try:
		id = int(dw_ent_id.get())
		if id < 1:
			raise Exception
		else:
			try:
				con = connect("ems.db")
				cursor = con.cursor()
				sql = "delete from ems where id = '%d'"
				id = int(dw_ent_id.get())
				cursor.execute(sql % (id))
				if cursor.rowcount == 1:
					con.commit()
					showinfo("Success", "Record Deleted")
					dw_ent_id.delete(0, END)
				else:
					con.rollback()
					showwarning("Absence", "Record does not exists")
					dw_ent_id.delete(0, END)
			except Exception as e:
				con.rollback()
				showerror("Mistake", e)
			finally:
				if con is not None:
					con.close()
	except Exception as e:
		showerror("Mistake", "Invalid ID")
		dw_ent_id.delete(0, END)

def f11():
	dw.withdraw()
	mw.deiconify()

dw = Toplevel(mw)
dw.title("Delete Emp")
dw.geometry("500x500+300+100")
dw.configure(bg="rosybrown")

dw_lbl_id = Label(dw, text="Enter ID", font=f)
dw_ent_id = Entry(dw, font=f)
dw_btn_delete = Button(dw, text="Delete", font=f, bd=2, width=12, command=f10)
dw_btn_back = Button(dw, text="Back", font=f, bd=2, width=12, command=f11)

dw_lbl_id.pack(pady=y)
dw_ent_id.pack(pady=y)
dw_btn_delete.pack(pady=y)
dw_btn_back.pack(pady=y)

dw.withdraw()

mw.mainloop()