#import python , tkinter , mysql librarires
import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
from tkcalendar import Calendar, DateEntry



#connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="cs"
)

#customers table create query for customers
customers_query = '''   
    CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    password VARCHAR(255),
    username VARCHAR(255)
    )
'''

#execute the query
with mydb.cursor() as cursor:
    cursor.execute(customers_query)
    #commit the query
    mydb.commit()

#salon services table create query for salon services
salon_services_query = '''   
    CREATE TABLE IF NOT EXISTS salon_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service VARCHAR(255),
    price DECIMAL(10, 2)
    )
'''
with mydb.cursor() as cursor:
    cursor.execute(salon_services_query)
    #commit
    mydb.commit()


#staff table create query for staffid, staffname, staffmail, staffphone, specialization
staff_query = '''   
    CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staffname VARCHAR(255),
    staffmail VARCHAR(255),
    staffphone VARCHAR(255),
    specialization VARCHAR(255)
    )
'''

with mydb.cursor() as cursor:
    cursor.execute(staff_query)



#salon appointments table create query for salon appointments
salon_appointments_query = '''   
    CREATE TABLE IF NOT EXISTS salon_appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    service_id INT,
    date DATE,
    time TIME,
    staff_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (service_id) REFERENCES salon_services(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
    )
'''

with mydb.cursor() as cursor:
    cursor.execute(salon_appointments_query)



#central salon class
class CentralSalon:
    def __init__(self, root):
        self.root = root
        self.root.title("Central Salon")
        self.root.geometry("1150x700")

        #default open login login
        self.login_screen()


    def login_screen(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Login")
        self.root.geometry("1150x700+0+0")

        #variables
        self.username = StringVar()
        self.password = StringVar()

        #frame
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=300, y=150, width=500, height=400)

        title = Label(login_frame, text="Login", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        lbl_username = Label(login_frame, text="Username", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=100)
        txt_username = Entry(login_frame, textvariable=self.username, font=("times new roman", 15), bg="lightgray").place(x=50, y=130)

        lbl_password = Label(login_frame, text="Password", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=180)
        txt_password = Entry(login_frame, textvariable=self.password, font=("times new roman", 15), bg="lightgray").place(x=50, y=210)

        btn_login = Button(login_frame, text="Login", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.validate_login).place(x=50, y=260)
        
        btn_register = Button(login_frame, text="Register", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.register_screen).place(x=250, y=260)

    def register_screen(self):


        #clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Register")
        self.root.geometry("950x800")


        #frame
        register_frame = Frame(self.root, bg="white")
        register_frame.place(x=200, y=50, width=500, height=700)

        title = Label(register_frame, text="Register", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        lbl_fullname = Label(register_frame, text="Full Name", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.fullname_entry = Entry(register_frame, font=("times new roman", 15), bg="lightgray")
        self.fullname_entry.place(x=50, y=130)

        lbl_lastname = Label(register_frame, text="Last Name", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=180)
        self.lastname_entry = Entry(register_frame, font=("times new roman", 15), bg="lightgray")
        self.lastname_entry.place(x=50, y=210)
    
        lbl_email = Label(register_frame, text="Email", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=260)
        self.email_entry = Entry(register_frame, font=("times new roman", 15), bg="lightgray")
        self.email_entry.place(x=50, y=290)

        lbl_phone = Label(register_frame, text="Phone", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=340)
        self.phone_entry = Entry(register_frame, font=("times new roman", 15), bg="lightgray")
        self.phone_entry.place(x=50, y=370)

        lbl_username = Label(register_frame, text="Username", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=420)
        self.username_entry = Entry(register_frame, font=("times new roman", 15), bg="lightgray")
        self.username_entry.place(x=50, y=450)

        lbl_password = Label(register_frame, text="Password", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=500)
        self.password_entry = Entry(register_frame, font=("times new roman", 15), bg="lightgray")
        self.password_entry.place(x=50, y=530)

        btn_register = Button(register_frame, text="Register", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.registerDB).place(x=50, y=570)
        
        btn_login = Button(register_frame, text="Login", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.login_screen).place(x=250, y=570)

    #autofill_username
    def autofill_username(self, event):
        email = self.email.get()
        username = email.split("@")[0]
        self.username.set(username)


    def registerDB(self):
        fullname = self.fullname_entry.get()
        lastname = self.lastname_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if fullname == "" or lastname == "" or email == "" or phone == "" or username == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("INSERT INTO customers (fullname, lastname, email, phone, username, password) VALUES (%s, %s, %s, %s, %s, %s)", (fullname, lastname, email, phone, username, password))
                mydb.commit()
                messagebox.showinfo("Success", "Registered successfully", parent=self.root)
                #back to login
                self.login_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
        


    #validate login
    def validate_login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM customers WHERE username = %s AND password = %s", (self.username.get(), self.password.get()))
                row = mycursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid username or password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Welcome", parent=self.root)
                    self.customer_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
        

    #customer dashboard
    def customer_dashboard(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Dashboard")
        self.root.geometry("1150x700")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(dashboard_frame, text="Dashboard", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        btn_services = Button(dashboard_frame, text="Services", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.services_screen).place(x=50, y=100)
        btn_appointments = Button(dashboard_frame, text="Appointments", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.appointments_screen).place(x=200, y=100)
        btn_logout = Button(dashboard_frame, text="Logout", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.login_screen).place(x=400, y=100)

    #services screen
    def services_screen(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Services")
        self.root.geometry("1150x700")

        #frame
        services_frame = Frame(self.root, bg="white")
        services_frame.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(services_frame, text="Services", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        btn_add_service = Button(services_frame, text="Add Service", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.add_service).place(x=50, y=100)
        btn_view_services = Button(services_frame, text="View Services", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.view_services).place(x=200, y=100)
        btn_back = Button(services_frame, text="Back", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.customer_dashboard).place(x=400, y=100)

    #add service
    def add_service(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Add Service")
        self.root.geometry("1150x700")

        #variables
        self.service = StringVar()
        self.price = StringVar()

        #frame
        add_service_frame = Frame(self.root, bg="white")
        add_service_frame.place(x=300, y=150, width=500, height=400)

        title = Label(add_service_frame, text="Add Service", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        lbl_service = Label(add_service_frame, text="Service", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=100)

        txt_service = Entry(add_service_frame, textvariable=self.service, font=("times new roman", 15), bg="lightgray").place(x=50, y=130)

        lbl_price = Label(add_service_frame, text="Price", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=180)

        txt_price = Entry(add_service_frame, textvariable=self.price, font=("times new roman", 15), bg="lightgray").place(x=50, y=210)

        btn_add_service = Button(add_service_frame, text="Add Service", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.add_serviceDB).place(x=50, y=260)

    #add service to database
    def add_serviceDB(self):
        service = self.service.get()
        price = self.price.get()

        if service == "" or price == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("INSERT INTO salon_services (service, price) VALUES (%s, %s)", (service, price))
                mydb.commit()
                messagebox.showinfo("Success", "Service added successfully", parent=self.root)
                self.services_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    #view services
    def view_services(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Services")
        self.root.geometry("1150x700")

        #frame
        view_services_frame = Frame(self.root, bg="white")
        view_services_frame.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(view_services_frame, text="Services", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM salon_services")
        rows = mycursor.fetchall()

        tree = ttk.Treeview(view_services_frame, columns=(1, 2), show="headings", height=10)
        tree.place(x=50, y=100)

        tree.heading(1, text="Service")
        tree.heading(2, text="Price")

        tree.column(1, width=200)
        tree.column(2, width=200)

        for row in rows:
            tree.insert("", "end", values=row)

        btn_back = Button(view_services_frame, text="Back", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.services_screen).place(x=400, y=100)

    #appointments screen
    def appointments_screen(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Appointments")
        self.root.geometry("1150x700")

        #frame
        appointments_frame = Frame(self.root, bg="white")
        appointments_frame.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(appointments_frame, text="Appointments", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        btn_book_appointment = Button(appointments_frame, text="Book Appointment", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.book_appointment).place(x=50, y=100)
        btn_view_appointments = Button(appointments_frame, text="View Appointments", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.view_appointments).place(x=200, y=100)
        btn_back = Button(appointments_frame, text="Back", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.customer_dashboard).place(x=400, y=100)

    #book appointment
    def book_appointment(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Book Appointment")
        self.root.geometry("1150x700")

        #variables
        self.service = StringVar()
        self.date = StringVar()
        self.time = StringVar()
        self.staff = StringVar()

        #frame
        book_appointment_frame = Frame(self.root, bg="white")
        book_appointment_frame.place(x=300, y=150, width=500, height=500)

        title = Label(book_appointment_frame, text="Book Appointment", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        lbl_service = Label(book_appointment_frame, text="Service", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=100)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM salon_services")
        rows = mycursor.fetchall()

        services = []
        for row in rows:
            services.append(row[1])

        self.service.set(services[0])

        service_dropdown = OptionMenu(book_appointment_frame, self.service, *services)
        service_dropdown.place(x=50, y=130)

        lbl_date = Label(book_appointment_frame, text="Date", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=180)

        date_entry = DateEntry(book_appointment_frame, textvariable=self.date, font=("times new roman", 15), bg="lightgray")
        date_entry.place(x=50, y=210)

        lbl_time = Label(book_appointment_frame, text="Time", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=260)

        time_entry = Entry(book_appointment_frame, textvariable=self.time, font=("times new roman", 15), bg="lightgray")
        time_entry.place(x=50, y=290)

        lbl_staff = Label(book_appointment_frame, text="Staff", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=50, y=340)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM staff")
        rows = mycursor.fetchall()

        staffs = []
        for row in rows:
            staffs.append(row[1])
        
        try:
            self.staff.set(staffs[0])
        except Exception as e:
            self.staff.set("")
            print("Error", e)


        staff_dropdown = OptionMenu(book_appointment_frame, self.staff, *staffs)
        staff_dropdown.place(x=50, y=370)

        btn_book_appointment = Button(book_appointment_frame, text="Book Appointment", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.book_appointmentDB).place(x=50, y=420)
        
        btn_back = Button(self.root, text="Back", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.appointments_screen).place(x=50, y=20)
    #book appointment to database
    def book_appointmentDB(self):
        service = self.service.get()
        date = self.date.get()
        time = self.time.get()
        staff = self.staff.get()

        if date == "" or time == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT id FROM salon_services WHERE service = %s", (service,))
                service_id = mycursor.fetchone()[0]

                mycursor.execute("SELECT id FROM staff WHERE staffname = %s", (staff,))
                staff_id = mycursor.fetchone()[0]

                mycursor.execute("INSERT INTO salon_appointments (customer_id, service_id, date, time, staff_id) VALUES (%s, %s, %s, %s, %s)", (1, service_id, date, time, staff_id))
                mydb.commit()
                messagebox.showinfo("Success", "Appointment booked successfully", parent=self.root)
                self.appointments_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    #view appointments
    def view_appointments(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Appointments")
        self.root.geometry("1150x700")

        #frame
        view_appointments_frame = Frame(self.root, bg="white")
        view_appointments_frame.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(view_appointments_frame, text="Appointments", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=150, y=30)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT salon_appointments.id, salon_services.service, salon_services.price, salon_appointments.date, salon_appointments.time, staff.staffname FROM salon_appointments INNER JOIN salon_services ON salon_appointments.service_id = salon_services.id INNER JOIN staff ON salon_appointments.staff_id = staff.id")
        rows = mycursor.fetchall()

        tree = ttk.Treeview(view_appointments_frame, columns=(1, 2, 3, 4, 5, 6), show="headings", height=10)
        tree.place(x=50, y=100)

        tree.heading(1, text="ID")
        tree.heading(2, text="Service")
        tree.heading(3, text="Price")
        tree.heading(4, text="Date")
        tree.heading(5, text="Time")
        tree.heading(6, text="Staff")

        tree.column(1, width=50)
        tree.column(2, width=200)
        tree.column(3, width=100)
        tree.column(4, width=100)
        tree.column(5, width=100)
        tree.column(6, width=200)

        for row in rows:
            tree.insert("", "end", values=row)

        btn_back = Button(view_appointments_frame, text="Back", font=("times new roman", 20, "bold"), bg="green", fg="white", command=self.appointments_screen).place(x=400, y=500)



#starter code
if __name__ == "__main__":
    root = Tk()
    app = CentralSalon(root)
    root.mainloop()