### MODULES AND PACKAGES ###

import tkinter as tk
from tkcalendar import Calendar,DateEntry
from tkinter import ttk
import sqlite3 as sq3


### CONSTANTS ###

MAIN_FONT = ("Consolas", 20)
SND_FONT = ("Consolas", 15)
MAIN_BG = "#383636"
MAIN_BTN_BG = "#474545"
MAIN_FG = "white"
data_file = './files/sampleDB.db'
icon_file = "./PhoneBook.ico"


### CLASSES AND METHODS ###

class App:


    def __init__(self):
        '''Object instance initialization function'''
        self.win = tk.Tk()
        self.win.resizable(False,False)
        self.win.title("Phone Book")
        self.win.geometry("800x500")
        self.win.configure(bg=MAIN_BG)
        self.win.iconbitmap(icon_file)
        self.conn = sq3.connect(data_file)
        self.curr = self.conn.cursor()
        self.phase1()


    def phase1(self):
        '''GUI of the Application'''

        self.clear()
        self.win.geometry("385x320")
        self.center()
        self.option_lab = tk.Label(self.win, text="Phone Book Options:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.option_lab.grid(row=0,column=0,columnspan=2,padx=45,pady=(40,20))
        self.display_btn = tk.Button(self.win, text="DISPLAY", command= lambda: self.display(self.all_data()), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.display_btn.grid(row=1,column=0,padx=10,pady=20)
        self.search_btn = tk.Button(self.win, text="SEARCH", command= lambda: self.search_phase1(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.search_btn.grid(row=1,column=1,padx=10,pady=20)
        self.include_btn = tk.Button(self.win, text="INCLUDE", command= lambda: self.include(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.include_btn.grid(row=2,column=0,padx=10,pady=20)
        self.delete_btn = tk.Button(self.win, text="DELETE", command= lambda: self.delete_phase1(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.delete_btn.grid(row=2,column=1,padx=10,pady=20)


    def format_data(self,data):
        '''Returns a formatted nested list containing all the data from the database for display'''

        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][3],data[i][4] = data[i][4],data[i][3]
        return data


    def all_data(self):
        '''Returns a nested list containing all the data from the database'''

        query = "SELECT * from AddressBook;"
        data_search = self.format_data(list(self.curr.execute(query)))
        return data_search

    def get_details(self):
        '''Gets and adds new Contact the the database (Backend)'''

        flag = 1
        fname = self.fname_ent.get()
        sname = self.sname_ent.get()
        phone = self.phone_ent.get()
        email = self.email_ent.get()
        address = self.address_ent.get()
        date = self.cal.get_date()

        if (phone.isdigit() == False):
            flag = 0
            self.phone_invalid_lab = tk.Label(self.win, text="(Not Valid)", fg=MAIN_FG, bg=MAIN_BG)
            self.phone_invalid_lab.grid(row=3,column=3)

        if (flag == 1):
            contact = Contact(fname,sname, phone, email, address, date)
            contact.storeDB()
            self.clear()
            self.phase1()

    def search_phase1(self):
        '''Searches contact in database using first name (Frontend)'''

        self.clear()
        self.win.geometry("470x250")
        self.center()

        fname_lab = tk.Label(self.win, text="Enter First name to Search:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        fname_lab.grid(row=0,column=0,columnspan=3,padx=20,pady=20)
        fname_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        fname_ent.grid(row=1,column=0,columnspan=3,padx=10,pady=10)
        back = tk.Button(self.win, text="Back", command = lambda: self.phase1(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        back.grid(row=2,column=0,padx=10,pady=10)
        submit_btn = tk.Button(self.win, text="Submit", command=lambda: self.search_phase2(fname_ent.get().lower()), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        submit_btn.grid(row=2,column=2,padx=10,pady=20)
        self.win.bind_all("<Return>", lambda event: self.search_phase2(fname_ent.get().lower()))


    def search_phase2(self, first_name):
        '''Searches and displays the contact using the display function (Backend)'''

        self.clear()
        self.win.geometry("620x450")
        self.center()

        data = []
        for data_item in self.all_data():
            if data_item[0].lower() == first_name:
                data.append(data_item)

        geo = "1400x"
        width = len(data)*100 + 100
        geo += str(width)

        self.display(data, geo)

    def include(self):
        '''New Contact creation form (Frontend)'''

        self.clear()
        self.win.geometry("620x450")
        self.center()
        self.fname_lab = tk.Label(self.win, text="First Name:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.fname_lab.grid(row=1,column=1,padx=10,pady=10)
        self.fname_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.fname_ent.grid(row=1,column=2,padx=10,pady=10)
        self.sname_lab = tk.Label(self.win, text="Second Name:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.sname_lab.grid(row=2,column=1,padx=10,pady=10)
        self.sname_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.sname_ent.grid(row=2,column=2,padx=10,pady=10)
        self.phone_lab = tk.Label(self.win, text="Phone Number:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.phone_lab.grid(row=3,column=1,padx=10,pady=10)
        self.phone_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.phone_ent.grid(row=3,column=2,padx=10,pady=10)
        self.email_lab = tk.Label(self.win, text="Email Address:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.email_lab.grid(row=4,column=1,padx=10,pady=10)
        self.email_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.email_ent.grid(row=4,column=2,padx=10,pady=10)
        self.address_lab = tk.Label(self.win, text="Home City:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.address_lab.grid(row=5,column=1,padx=10,pady=10)
        self.address_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.address_ent.grid(row=5,column=2,padx=10,pady=10)
        self.bday_lab = tk.Label(self.win, text="Birth Date:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.bday_lab.grid(row=6,column=1,padx=10,pady=10)
        self.cal = DateEntry(self.win, font=MAIN_FONT, width= 16, background= MAIN_BTN_BG, foreground= MAIN_FG,bd=2)
        self.cal.grid(row=6,column=2,padx=10,pady=10)
        self.back = tk.Button(self.win, text="Back", command = lambda: self.phase1(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.back.grid(row=7,column=1,padx=10,pady=10)
        self.submit = tk.Button(self.win, text="Submit", command = lambda: self.get_details(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        self.submit.grid(row=7,column=2,padx=10,pady=10)
        self.win.bind_all("<Return>", lambda event: self.self.get_details())


    def delete_phase2(self,phone_number):
        '''Deleteion from database by sqlite3 queries'''

        self.conn = sq3.connect(data_file)
        self.curr = self.conn.cursor()
        query = f'''DELETE FROM AddressBook WHERE PhoneNo = {phone_number};'''
        self.curr.execute(query)
        self.conn.commit()
        self.clear()
        self.phase1()


    def delete_phase1(self):
        '''Getting phone number to identify contact and delete in from AddressBook'''

        self.clear()
        self.win.geometry("470x250")
        self.center()
        del_lab = tk.Label(self.win, text="Enter Phone Number to Delete:", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        del_lab.grid(row=0,column=0,columnspan=3,padx=20,pady=20)
        phone_ent = tk.Entry(self.win, font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        phone_ent.grid(row=1,column=0,columnspan=3,padx=10,pady=10)
        back = tk.Button(self.win, text="Back", command = lambda: self.phase1(), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        back.grid(row=2,column=0,padx=10,pady=10)
        submit_btn = tk.Button(self.win, text="Submit", command=lambda: self.delete_phase2(phone_ent.get()), font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BTN_BG)
        submit_btn.grid(row=2,column=2,padx=10,pady=20)
        self.win.bind_all("<Return>", lambda event: self.delete_phase2())


    def display(self,data,geo="1400x600"):
        '''Genralised function to display all contacts or selected from search'''


        def _on_mouse_wheel(event):
            my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        self.win.geometry(geo)
        self.clear()
        self.win.configure(bg=MAIN_BG)
        self.center()

        total = len(data)

        main_frame = tk.Frame(self.win, bg=MAIN_BG)
        main_frame.pack(fill=tk.BOTH, expand=1)
        my_canvas = tk.Canvas(main_frame, bg=MAIN_BG)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        my_scrollbary = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        my_canvas.configure(yscrollcommand=my_scrollbary.set)

        my_scrollbarx = ttk.Scrollbar(self.win, orient=tk.HORIZONTAL, command=my_canvas.xview)
        my_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        my_canvas.configure(xscrollcommand=my_scrollbarx.set)
        
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
        second_frame = tk.Frame(my_canvas, bg=MAIN_BG)
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")
        my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        self.sno_lab = tk.Label(second_frame, text="S.No", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.sno_lab.grid(row=0,column=0,padx=(20,0),pady=(40,20))
        self.fname_lab = tk.Label(second_frame, text="First Name", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.fname_lab.grid(row=0,column=1,padx=(40,0),pady=(40,20))
        self.sname_lab = tk.Label(second_frame, text="Second Name", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.sname_lab.grid(row=0,column=2,padx=(40,0),pady=(40,20))
        self.phone_lab = tk.Label(second_frame, text="Phone Num", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.phone_lab.grid(row=0,column=3,padx=(40,0),pady=(40,20))
        self.email_lab = tk.Label(second_frame, text="Email", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.email_lab.grid(row=0,column=4,padx=(40,0),pady=(40,20))
        self.address_lab = tk.Label(second_frame, text="Address", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.address_lab.grid(row=0,column=5,padx=(40,0),pady=(40,20))
        self.birthday_lab = tk.Label(second_frame, text="Birthdate", font=MAIN_FONT, fg=MAIN_FG, bg=MAIN_BG)
        self.birthday_lab.grid(row=0,column=6,padx=(40,0),pady=(40,20))

        for r in range(total):
            sno_lab = tk.Label(second_frame, text=r+1, font=SND_FONT, fg=MAIN_FG, bg=MAIN_BG)
            sno_lab.grid(row=r+1,column=0,pady=(40,20))
            for c in range(6):
                temp_lab = tk.Label(second_frame, text=data[r][c], font=SND_FONT, fg=MAIN_FG, bg=MAIN_BG)
                temp_lab.grid(row=r+1,column=c+1,padx=(40,0),pady=(40,20))
        
        self.win.bind_all("<Escape>", lambda event: self.phase1())


    def run(self):
        '''Starts the GUI application'''

        self.win.mainloop()
        self.conn.close()
    

    def clear(self):
        '''Deletes the widgets on the window'''

        for wid in self.win.winfo_children():
            wid.destroy()

    def center(self):
        '''Centers a tkinter window'''

        self.win.update_idletasks()
        width = self.win.winfo_width()
        frm_width = self.win.winfo_rootx() - self.win.winfo_x()
        win_width = width + 2 * frm_width
        height = self.win.winfo_height()
        titlebar_height = self.win.winfo_rooty() - self.win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.win.winfo_screenwidth() // 2 - win_width // 2
        y = self.win.winfo_screenheight() // 2 - win_height // 2
        self.win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.win.deiconify()


class Contact:


    def __init__(self,fname,sname, phone, email, address, date):
        '''Contact-object instance initialization function'''

        self.first_name = fname
        self.second_name = sname
        self.phone_number = phone
        self.address = address
        self.birthday = date
        self.email = email


    def storeDB(self):
        '''Stores the inputted data into the sqlite3 database'''

        self.conn = sq3.connect(data_file)
        self.curr = self.conn.cursor()
        query = f'''INSERT INTO AddressBook VALUES ("{self.first_name}", "{self.second_name}", {self.phone_number}, "{self.address}", "{self.email}", "{self.birthday}");'''
        self.curr.execute(query)
        self.conn.commit()


### MAIN SECTION ###

if __name__ == "__main__":
    app = App()
    app.run()


### MISC SECTION ###

def queries():

    conn = sq3.connect('./files/sampleDB.db')
    curr = conn.cursor()

    # DELETE (DROP) TABLE QUERY:
    curr.execute("DROP TABLE AddressBook;")

    # CREATE TABLE QUERY:
    query = "CREATE TABLE AddressBook(\
    FirstName TEXT, LastName TEXT, PhoneNo INTEGER, Address TEXT,\
    Email BLOB, BirthDay TEXT);"
    curr.execute(query)

    # INSERT QUERY:
    curr.execute(f'''INSERT INTO AddressBook VALUES ("{fname}", "{sname}", "{num}", "{city}", "{email}", "{date}")''')

    conn.commit()
    conn.close()