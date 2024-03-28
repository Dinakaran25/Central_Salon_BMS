#import python , tkinter , mysql librarires
import random,smtplib,string
import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import messagebox,Frame, Label, Entry, Button
from tkinter import ttk, font as tkfont
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from datetime import datetime as dt
from tkcalendar import DateEntry
from email.mime.text import MIMEText
from datetime import timedelta
from tkinter import messagebox
from tkinter import ttk
import datetime




#connect to the database 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root$123",
    database="central_salon"
)

#customers table 
customers_query = '''   
    CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255)
    
    )
'''

#execute the query
with mydb.cursor() as cursor:
    cursor.execute(customers_query)
    #commit the query
    mydb.commit()

#salon services table 
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


#staff table 
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



#salon appointments table 
salon_appointments_query = '''   
    CREATE TABLE IF NOT EXISTS salon_appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    service_id INT,
    date DATE,
    time TIME,
    staff_id INT,
    name VARCHAR(255),
    checkin TINYINT DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (service_id) REFERENCES salon_services(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
    )
'''

with mydb.cursor() as cursor:
    cursor.execute(salon_appointments_query)



#central salon class
class CentralSalon:
    # how to inherit tooltip class

    def __init__(self, root):
        self.root = root
        self.root.title("CentralSalon")
        self.root.geometry("1150x700")
        self.resetpassword=False

        #default open login login
        self.login_screen()

    

    def login_screen(self):

        #clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Login")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/loginnew.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #variables
        self.username = StringVar()
        self.password = StringVar()
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        

        #frame
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(x=125, y=150, width=400, height=450)

        welcome_label = tk.Label(self.login_frame, text="WELCOME", font=("Calibri", 25, "bold"), bg="white", fg="#b89b3f").place(x=120, y=0)
        

        self.logo_image = ImageTk.PhotoImage(Image.open("Images/central_logo.png").resize((100, 100), Image.LANCZOS))
        Label(self.login_frame,image=self.logo_image, bg="white").place(x=150, y=50)

        title = Label(self.login_frame, text="Login", font=("Calibri", 25, "bold"), bg="white", fg="#b89b3f").place(x=25, y=125)

        lbl_username = Label(self.login_frame, text="Username:", font=("Calibri", 18,"bold"), bg="white", fg="#b89b3f").place(x=10, y=170)
        self.username_entry = Entry(self.login_frame, textvariable=self.username, font=("Calibri", 12), bg="#ECECEC").place(x=140, y=180)
        # self.username_entry.insert(0, "Username")
        # self.username_entry.bind('<FocusIn>', self.removeusernametext)
        # self.username_entry.bind('<FocusOut>', self.removeusernametext)
        

        lbl_password = Label(self.login_frame, text="Password:", font=("Calibri", 18, "bold"), bg="white", fg="#b89b3f").place(x=10, y=215)
        self.password_entry = Entry(self.login_frame, textvariable=self.password, font=("Calibri", 12), bg="#ECECEC", show="*")
        self.password_entry.place(x=140, y=220)
        # self.password_entry.insert(0, "Password")
        # self.password_entry.bind('<FocusIn>', self.removepasswordtext)
        # self.password_entry.bind('<FocusOut>', self.removepasswordtext)

        show_icon_image = Image.open("Images/show_icon.png")
        show_icon_resized = show_icon_image.resize((25, 25), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.show_icon = ImageTk.PhotoImage(show_icon_resized)

        # Open and resize the hide icon
        hide_icon_image = Image.open("Images/hide_icon.png")
        hide_icon_resized = hide_icon_image.resize((25, 25), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.hide_icon = ImageTk.PhotoImage(hide_icon_resized)


        # Create a button to toggle password visibility
        self.toggle_button = tk.Button(self.login_frame, image=self.show_icon, command=self.toggle_password_visibility, borderwidth=0,highlightthickness=0, bg="white", activebackground="white")
        self.toggle_button.place(x=315, y=220)

        self.forgot_password_link = tk.Label(self.login_frame, text="Forgot Password?",font=("Calibri", 12), fg="blue", cursor="hand2",bg="white")
        self.forgot_password_link.pack()
        self.forgot_password_link.bind("<Button-1>", lambda e: self.reset_password())
        self.forgot_password_link.place(x=140, y=253)
        self.forgot_password_link.bind("<Enter>", lambda e: self.forgot_password_link.config(fg="#b89b3f"))
        self.forgot_password_link.bind("<Leave>", lambda e: self.forgot_password_link.config(fg="blue"))

        self.login_button = Button(self.login_frame, text="Login", font=("Calibri", 18, "bold"), bg="#b89b3f", fg="white",cursor="hand2", command=self.validate_login).place(x= 150, y=300)
    
        #self.login_button = Button(self.login_frame, text="Login", font=("Calibri", 18, "bold"), bg="#b89b3f", fg="white",cursor="hand2", command=self.show_update_password_form).place(x=100, y=300)
        
        title = Label(self.login_frame, text="Don't have an account?", font=("Calibri", 12), fg="black", bg="white", cursor="hand2")
        title.place(x=50, y=400)
        
                
        self.register_text = Label(self.login_frame, text="Register now", font=("Calibri", 12), fg="blue", bg="white", cursor="hand2")
        self.register_text.place(x=210, y=400)
        self.register_text.bind("<Button-1>", lambda e: self.register_screen())
        self.register_text.bind("<Enter>", lambda e: self.register_text.config(fg="#b89b3f"))
        self.register_text.bind("<Leave>", lambda e: self.register_text.config(fg="blue"))
    
    # def removeusernametext(self, event):
    #     if self.username_entry.get() == "Username":
    #         self.username_entry.delete(0, "end")
    #         self.username_entry.config(fg="white")
    #     elif self.username_entry.get() == "":
    #         self.username_entry.insert(0, "Username")
    #         self.username_entry.config(fg="white") 
    # def removepasswordtext(self, event):
    #     if self.password_entry.get() == "Password":
    #         self.password_entry.delete(0, "end")
    #         self.password_entry.config(fg="white")
    #         self.password_entry.config(show="*")
    #     elif self.password_entry.get() == "":
    #         self.password_entry.insert(0, "Password")
    #         self.password_entry.config(show="")
    #         self.password_entry.config(fg="white") 

    def toggle_password_visibility(self):
        if self.password_visible:
            # Hide the password and update the button icon
            self.password_entry.config(show="*")
            self.toggle_button.config(image=self.show_icon)
            self.password_visible = False
        else:
            # Show the password and update the button icon
            self.password_entry.config(show="")
            self.toggle_button.config(image=self.hide_icon)
            self.password_visible = True

    def reset_password(self):
        username = self.username.get()  # Make sure to use .get() for StringVar()
        if not username:
            messagebox.showerror("Error", "Please enter your username first.")
            return
        self.new_password = self.generate_new_password()
        email_address = self.get_email_address(username)
        if email_address:
            try:
                cursor = mydb.cursor()
                if cursor is not None:
                    query = 'SELECT id FROM customers WHERE email = %s'
                    cursor.execute(query, (email_address,))
                    customer_id = cursor.fetchone()[0]
                    if customer_id:
                        query = 'UPDATE customers SET password = %s WHERE id = %s'
                        self.resetpassword=TRUE
                        # print(self.new_password,type(self.new_password))
                        # print(customer_id,type(customer_id))
                        cursor.execute(query, (self.new_password, int(customer_id)))
                        mydb.commit()
                        self.send_email(email_address, self.new_password)
                        messagebox.showinfo("Success", f"New password was sent to the email address associated with {username}: {email_address}")
                        self.login_screen()
                    else:
                        messagebox.showerror("Error", "No customer found with this email.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "No email address found for this username.")

    def generate_new_password(self):
        password_length = 10
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length))
        return new_password

    def get_email_address(self, username):
        email_address = None  # Initialize email_address at the start
        try:
            cursor = mydb.cursor()  # Assuming mydb is correctly set up to return a connection object
            cursor.execute("SELECT email FROM customers WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                email_address = result[0]
            else:
                print("No email address found for this username.")
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            if 'cursor' in locals() and cursor:  # Check if cursor was successfully created
                cursor.close()
        return email_address
    
    def send_email(self, email_address, new_password):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'central.salon.1@gmail.com'
        smtp_password = 'qirdsouhpvmxhzlu'
        message = MIMEText(f""" 
        Hi,

        You've requested to reset your password. Here's your temporary password.

        Temporary Password: {new_password}

        Please use this to log in and then change it to something new and secure.

        If you didn't ask to reset your password, please let us know.

        Thanks,
        Central Salon""")

        message['Subject'] = 'Your Temporary Password'
        message['From'] = smtp_user
        message['To'] = email_address
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [email_address], message.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")

    def show_update_password_form(self):
        #destory everything and create same as login
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Update Password")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/loginnew.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.password_visible1 = False
        self.password_visible2 = False
        self.password_visible3 = False

        #frame
        self.update_password_frame = Frame(self.root, bg="white")
        self.update_password_frame.place(x=125, y=150, width=400, height=400)

        title = Label(self.update_password_frame, text="Change Password", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f").place(x=25, y=10)
        
        self.logo_image = ImageTk.PhotoImage(Image.open("Images/central_logo.png").resize((100, 100), Image.LANCZOS))
        Label(self.update_password_frame,image=self.logo_image, bg="white").place(x=150, y=70) 
        
        lbl_current_password = Label(self.update_password_frame, text="Temporary Password:", font=("Calibri", 12,"bold"), bg="white", fg="#b89b3f").place(x=10, y=170)
        self.current_password_entry = Entry(self.update_password_frame, font=("Calibri", 12), bg="#ECECEC", show="*")
        self.current_password_entry.place(x=10, y=200)

        self.toggle_button1 = tk.Button(self.update_password_frame, image=self.show_icon, command=self.toggle_password_visibility1, borderwidth=0,highlightthickness=0, bg="white",activebackground="white")
        self.toggle_button1.place(x=200, y=200)

        lbl_new_password = Label(self.update_password_frame, text="New Password:", font=("Calibri", 12,"bold"), bg="white", fg="#b89b3f").place(x=10, y=220)
        self.new_password_entry = Entry(self.update_password_frame, font=("Calibri", 12), bg="#ECECEC", show="*")
        self.new_password_entry.place(x=10, y=250)

        self.toggle_button2 = tk.Button(self.update_password_frame, image=self.show_icon, command=self.toggle_password_visibility2, borderwidth=0,highlightthickness=0, bg="white",activebackground="white")
        self.toggle_button2.place(x=200, y=250)    

        lbl_confirm_new_password = Label(self.update_password_frame, text="Confirm New Password:", font=("Calibri", 12,"bold"), bg="white", fg="#b89b3f").place(x=10, y=270)
        self.confirm_new_password_entry = Entry(self.update_password_frame, font=("Calibri", 12), bg="#ECECEC", show="*")
        self.confirm_new_password_entry.place(x=10, y=300)

        self.toggle_button3 = tk.Button(self.update_password_frame, image=self.show_icon, command=self.toggle_password_visibility3, borderwidth=0,highlightthickness=0, bg="white",activebackground="white")
        self.toggle_button3.place(x=200, y=300)

        self.update_password_button = Button(self.update_password_frame, text="Update Password", font=("Calibri", 18, "bold"), bg="#b89b3f", fg="white", command=self.update_password).place(x=50, y=340)
    
    
    def toggle_password_visibility1(self):
        if self.password_visible1:
            self.current_password_entry.config(show="*")
            self.toggle_button1.config(image=self.show_icon)
            self.password_visible1 = False
        else:
            self.current_password_entry.config(show="")
            self.toggle_button1.config(image=self.hide_icon)
            self.password_visible1 = True

    def toggle_password_visibility2(self):
        if self.password_visible2:
            self.new_password_entry.config(show="*")
            self.toggle_button2.config(image=self.show_icon)
            self.password_visible2 = False
        else:
            self.new_password_entry.config(show="")
            self.toggle_button2.config(image=self.hide_icon)
            self.password_visible2 = True

    def toggle_password_visibility3(self):
        if self.password_visible3:
            self.confirm_new_password_entry.config(show="*")
            self.toggle_button3.config(image=self.show_icon)  # Update the button name to toggle_button3
            self.password_visible3 = False
        else:
            self.confirm_new_password_entry.config(show="")
            self.toggle_button3.config(image=self.hide_icon)  # Update the button name to toggle_button3
            self.password_visible3 = True

    def update_password(self):
        current_password=self.current_password_entry.get()
        new_password=self.new_password_entry.get()
        confirm_new_password=self.confirm_new_password_entry.get()
        userid=self.userid

        #print(current_password,new_password,confirm_new_password)

        if new_password != confirm_new_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return

        try:
            cursor = mydb.cursor()
            #print(self.new_password,current_password)
            if self.new_password == current_password:
                if cursor is not None:
                    query = 'UPDATE customers SET password = %s WHERE id = %s'
                    cursor.execute(query, (new_password, userid))
                    mydb.commit()
                    messagebox.showinfo("Success", "Your password has been updated successfully.")
                    self.customer_dashboard()
                else:
                    messagebox.showerror("Error", "Failed to update password.")
            else:
                messagebox.showerror("Error", "Current password is incorrect.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")     
            
               
    #validate login
    def validate_login(self):
        self.username = self.username.get()
        self.password = self.password.get()
        if self.username == "" or self.password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.username=="admin" and self.password=="admin":
            self.admin_dashboard()
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM customers WHERE username = %s AND password = %s", (self.username, self.password))
                row = mycursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid username or password", parent=self.root)
                else:
                    if self.resetpassword:
                        self.userid = row[0]
                        self.show_update_password_form()
                    else:
                        welcome_message = f"Welcome, {self.username}!"
                        messagebox.showinfo("Login Success", welcome_message, parent=self.root)
                        
                        #save userid
                        self.userid = row[0]
                        self.customer_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
                

    def register_screen(self):
        #clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Register")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/loginnew.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #frame
        register_frame = Frame(self.root, bg="white")
        register_frame.place(x=125, y=130, width=400, height=500)

        self.email_var = StringVar()
        self.username_var = StringVar()

        title = Label(register_frame, text="Register", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f").place(x=100, y=10)

        lbl_fullname = Label(register_frame, text="First Name:", font=("Calibri", 15, "bold"), bg="white", fg="#b89b3f").place(x=30, y=60)
        self.fullname_entry = Entry(register_frame, font=("Calibri", 12), bg="#ECECEC")
        self.fullname_entry.place(x=30, y=90)

        lbl_lastname = Label(register_frame, text="Last Name:", font=("Calibri", 15, "bold"), bg="white", fg="#b89b3f").place(x=30, y=120)
        self.lastname_entry = Entry(register_frame, font=("Calibri", 12), bg="#ECECEC")
        self.lastname_entry.place(x=30, y=150)
    
        lbl_email = Label(register_frame, text="Email:", font=("Calibri", 15, "bold"), bg="white", fg="#b89b3f").place(x=30, y=180)
        self.email_entry = Entry(register_frame, font=("Calibri", 12), bg="#ECECEC")
        self.email_entry.place(x=30, y=210)
        self.email_entry.bind('<KeyRelease>', self.autofill_username)

        lbl_phone = Label(register_frame, text="Phone:", font=("Calibri", 15, "bold"), bg="white", fg="#b89b3f").place(x=30, y=240)
        self.phone_entry = Entry(register_frame, font=("Calibri", 12), bg="#ECECEC")
        self.phone_entry.place(x=30, y=270)

        lbl_username = Label(register_frame, text="Username:", font=("Calibri", 15, "bold"), bg="white", fg="#b89b3f").place(x=30, y=300)
        self.username_entry = Entry(register_frame, font=("Calibri", 12), bg="#ECECEC")
        self.username_entry.place(x=30, y=330)

        lbl_password = Label(register_frame, text="Password:", font=("Calibri", 15, "bold"), bg="white", fg="#b89b3f").place(x=30, y=360)
        self.password_entry = Entry(register_frame, font=("Calibri", 12), bg="#ECECEC",show="*")
        self.password_entry.place(x=30, y=390)

        self.toggle_button = tk.Button(register_frame, image=self.show_icon, command=self.toggle_password_visibility, borderwidth=0,highlightthickness=0, bg="white",activebackground="white")
        self.toggle_button.place(x=210, y=390)

        self.register_button = Button(register_frame, text="Register", font=("Calibri", 18, "bold"), bg="#b89b3f", fg="white", command=self.registerDB).place(x=150, y=440)
        
        back_icon_image = Image.open("Images/back_icon.png")
        back_icon_resized = back_icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.back_icon = ImageTk.PhotoImage(back_icon_resized)

        self.left_button = tk.Button(register_frame, image=self.back_icon, command=self.login_screen, borderwidth=0, highlightthickness=0, bg="white", activebackground="white")
        self.left_button.place(x=10, y=10)

    #autofill_username
    def autofill_username(self, event):
        email = self.email_entry.get()
        username = email.split("@")[0]
        self.username_entry.delete(0, 'end')  # Clear the current content
        self.username_entry.insert(0, username)


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
                mycursor.execute("INSERT INTO customers (firstname, lastname, email, phone, username, password) VALUES (%s, %s, %s, %s, %s, %s)", (fullname, lastname, email, phone, username, password))
                mydb.commit()
                messagebox.showinfo("Success", "Registered successfully.!!", parent=self.root)
                #back to login
                self.login_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
        


    def customer_dashboard(self):
        #clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Customer Dashboard")
        self.root.geometry("1150x700+0+0")
        
        self.bg_image = Image.open("Images/home_page.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menu frame (directly on self.root to overlay the background image)
        menu_frame = Frame(self.root, bg="lightgrey", bd=0)  # bd=0 to remove border if desired
        menu_frame.place(x=30, y=0, width=300, height=700)

        welcome_text = f"Welcome, {self.username}!" 
        title = Label(self.root, text=welcome_text, font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f", bd=0).place(x=450, y=50)

        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 30, "bold"), bg="lightgrey", fg="black").place(x=100, y=30)


        #book appointment button

        self.book_appointment_button = tk.Label(self.root, text="Book Appointment", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2")
        self.book_appointment_button.pack()
        self.book_appointment_button.bind("<Button-1>", lambda e: self.book_appointment())
        self.book_appointment_button.place(x=75, y=150)
        self.book_appointment_button.bind("<Enter>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="#b89b3f"))
        self.book_appointment_button.bind("<Leave>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="black"))


        #view my appointments button
        self.view_appointments_button = Button(self.root, text="View My Appointments", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black",cursor="hand2", activebackground='lightgrey', command=self.view_appointments)
        self.view_appointments_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_appointments_button.place(x=75, y=200)
        self.view_appointments_button.bind("<Enter>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_appointments_button.bind("<Leave>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg="black"))

        #view services button
        self.view_services_button = Button(self.root, text="View Services", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.view_services_customer)
        self.view_services_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_services_button.place(x=75, y=250)
        self.view_services_button.bind("<Enter>", lambda e: self.view_services_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_services_button.bind("<Leave>", lambda e: self.view_services_button.config(bg="lightgrey", fg="black"))

        #my profile button
        self.my_profile_button = Button(self.root, text="My Profile", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.my_profile)
        self.my_profile_button.config(relief='flat', bd=0, highlightthickness=0)
        self.my_profile_button.place(x=75, y=300)
        self.my_profile_button.bind("<Enter>", lambda e: self.my_profile_button.config(bg="lightgrey", fg='#b89b3f'))
        self.my_profile_button.bind("<Leave>", lambda e: self.my_profile_button.config(bg="lightgrey", fg="black"))

        #logout button
        self.logout_button = Button(self.root, text="Logout", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.login_screen)
        self.logout_button.config(relief='flat', bd=0, highlightthickness=0)
        self.logout_button.place(x=75, y=350)
        self.logout_button.bind("<Enter>", lambda e: self.logout_button.config(bg="lightgrey", fg='#b89b3f'))
        self.logout_button.bind("<Leave>", lambda e: self.logout_button.config(bg="lightgrey", fg="black"))


    def book_appointment(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Book Appointment")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/dashboard.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menu frame (directly on self.root to overlay the background image)
        menu_frame = Frame(self.root, bg="lightgrey", bd=0)  # bd=0 to remove border if desired
        menu_frame.place(x=30, y=0, width=300, height=700)

        title = Label(self.root, text="Book Appointment", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f",bd=0).place(x=450, y=30)

        back_icon_image = Image.open("Images/back_icon.png")
        back_icon_resized = back_icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.back_icon = ImageTk.PhotoImage(back_icon_resized)

        self.left_button = tk.Button(self.root, image=self.back_icon, command=self.customer_dashboard, borderwidth=0, highlightthickness=0, bg="white", activebackground="white")
        self.left_button.place(x=350, y=30)

        #menu label buttons
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 30, "bold"), bg="lightgrey", fg="black").place(x=100, y=30)


        #book appointment button

        self.book_appointment_button = tk.Label(self.root, text="Book Appointment", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2")
        self.book_appointment_button.pack()
        self.book_appointment_button.bind("<Button-1>", lambda e: self.book_appointment())
        self.book_appointment_button.place(x=75, y=150)
        self.book_appointment_button.bind("<Enter>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="#b89b3f"))
        self.book_appointment_button.bind("<Leave>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="black"))


        #view my appointments button
        self.view_appointments_button = Button(self.root, text="View My Appointments", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black",cursor="hand2", activebackground='lightgrey', command=self.view_appointments)
        self.view_appointments_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_appointments_button.place(x=75, y=200)
        self.view_appointments_button.bind("<Enter>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_appointments_button.bind("<Leave>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg="black"))

        #view services button
        self.view_services_button = Button(self.root, text="View Services", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.view_services_customer)
        self.view_services_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_services_button.place(x=75, y=250)
        self.view_services_button.bind("<Enter>", lambda e: self.view_services_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_services_button.bind("<Leave>", lambda e: self.view_services_button.config(bg="lightgrey", fg="black"))

        #my profile button
        self.my_profile_button = Button(self.root, text="My Profile", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.my_profile)
        self.my_profile_button.config(relief='flat', bd=0, highlightthickness=0)
        self.my_profile_button.place(x=75, y=300)
        self.my_profile_button.bind("<Enter>", lambda e: self.my_profile_button.config(bg="lightgrey", fg='#b89b3f'))
        self.my_profile_button.bind("<Leave>", lambda e: self.my_profile_button.config(bg="lightgrey", fg="black"))

        #logout button
        self.logout_button = Button(self.root, text="Logout", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.login_screen)
        self.logout_button.config(relief='flat', bd=0, highlightthickness=0)
        self.logout_button.place(x=75, y=350)
        self.logout_button.bind("<Enter>", lambda e: self.logout_button.config(bg="lightgrey", fg='#b89b3f'))
        self.logout_button.bind("<Leave>", lambda e: self.logout_button.config(bg="lightgrey", fg="black"))

        
        #left frame for booking appointment
        left_frame = Frame(self.root, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #select service combobox
        services=[]
        mycursor = mydb.cursor()
        mycursor.execute("SELECT service FROM salon_services")
        rows = mycursor.fetchall()
        for row in rows:
            services.append(row[0])
        
        self.select_service_label = Label(left_frame, text="Select Service", font=("Calibri", 15,"bold"), bg="white")
        self.select_service_label.place(x=50, y=40)

        self.services_combobox = Combobox(left_frame, values=services, font=("Calibri", 15), state="readonly")
        self.services_combobox.set("Select Service")
        self.services_combobox.place(x=50, y=70)


        self.date_label = Label(left_frame, text="Select Date", font=("Calibri", 15,"bold"), bg="white")
        self.date_label.place(x=50, y=110)

        # Modify the DateEntry widget to use the desired date format
        
        self.date_entry = DateEntry(left_frame, font=("Calibri", 12), date_pattern='mm-dd-yyyy', mindate=datetime.date.today(),
                                    weekend_background='lightgray', weekend_foreground='black',
                                    othermonth_webackground='lightgray', othermonth_foreground='dim gray',
                                    othermonth_weforeground='dim gray')
        self.date_entry.place(x=50, y=140)
        self.date_entry.configure(state='readonly', disabledbackground='lightgray')
        # Binding to the '<<DateEntrySelected>>' event to check for Sundays
        self.date_entry.bind("<<DateEntrySelected>>", self.check_for_sunday)


        #select time
        self.time_label = Label(left_frame, text="Select Time", font=("Calibri", 15,"bold"), bg="white")
        self.time_label.place(x=50, y=180)

        # Time Combobox
        self.time_combobox = ttk.Combobox(left_frame, values=["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"], font=("Calibri", 15), state="readonly")
        self.time_combobox.set("Select Time")
        self.time_combobox.place(x=50, y=210)

        # Name
        self.name_label = Label(left_frame, text="Name", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=260)
        self.name_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.name_entry.place(x=50, y=290)

        self.price_label = Label(left_frame, text="Price", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=330)
        self.price_entry = Entry(left_frame,font=("Calibri", 15), bg="white", fg="black")
        self.price_entry.place(x=50, y=360)

        # Bind the combobox selection event to the callback function
        self.services_combobox.bind("<<ComboboxSelected>>", self.update_price)

        #confirm button
        self.confirm_button = Button(left_frame, text="Confirm", font=("Calibri", 15, "bold"), bg="#b89b3f", fg="white", command=lambda: self.confirm_appointment(self.username)).place(x=100, y=420)

    def check_for_sunday(self, event):
        selected_date = self.date_entry.get_date()
        if selected_date and selected_date.weekday() == 6:
            messagebox.showerror("Error", "Salon is closed on Sundays. Please select another date.", parent=self.root)
            self.date_entry.set_date(None)

            
    def update_price(self, event):
        service = self.services_combobox.get()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT price FROM salon_services WHERE service = %s", (service,))
        price = mycursor.fetchone()[0]
        self.price_entry.config(state="normal")
        self.price_entry.delete(0, END)
        self.price_entry.insert(0, "$" + str(price))
        self.price_entry.config(state="readonly")
             

    def confirm_appointment(self,username):
        service = self.services_combobox.get()
        date = self.date_entry.get()
        time = self.time_combobox.get()
        name = self.name_entry.get()
        email_address = self.get_email_address(username)  # Assuming this method retrieves the current user's email

        # Attempt to convert date and time to the desired format
        try:
            print(f"Date input: '{date}', Time input: '{time}'")
            formatted_date = dt.strptime(date, "%m-%d-%Y").strftime("%Y-%m-%d")
            formatted_time = dt.strptime(time, "%I:%M %p").strftime("%H:%M:%S")
            print(formatted_date, formatted_time)


        except ValueError as e:
            messagebox.showerror("Error", "Invalid date or time format", parent=self.root)
            return

        if service == "Select Service" or not date or not time or not name:
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if not email_address:
            messagebox.showerror("Error", "No email address found for this username.")
            return

        booking_details = {
            'date_time': f"{formatted_date} at {formatted_time}",
            'services': [service],  # Assuming a single service for simplicity; adjust as needed
        }
        try:
            mycursor = mydb.cursor()
            userid=self.userid
            mycursor.execute("SELECT id FROM salon_services WHERE service = %s", (service,))
            service_id = mycursor.fetchone()[0]

            #insert into database
            mycursor.execute("INSERT INTO salon_appointments (customer_id, service_id, date, time, name) VALUES (%s, %s, %s, %s, %s)", (userid, service_id, formatted_date, formatted_time, name))
            mydb.commit()

            self.send_booking_confirmation_email(email_address, booking_details)

            messagebox.showinfo("Success", "Appointment Booked Successfully. A confirmation email has been sent.", parent=self.root)
            # Assuming this method resets the view or takes the user back to the dashboard
            self.customer_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
        
            
    def send_booking_confirmation_email(self, email_address, booking_details):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'central.salon.1@gmail.com'
        smtp_password = 'qirdsouhpvmxhzlu'  # Ideally, this should be securely stored and retrieved
        
        # Construct the booking details message
        booking_info = f"""
        Dear Customer,
        
        Thank you for booking with Central Salon!
        
        Here are your booking details:
        - Date and Time: {booking_details['date_time']}
        - Services: {', '.join(booking_details['services'])}
        - Price: {self.price_entry.get()}
        
        If you need to cancel or reschedule, please contact us at least an hour in advance.
        
        We look forward to serving you,
        Central Salon.
        """
        
        message = MIMEText(booking_info)
        message['Subject'] = 'Booking Confirmation'
        message['From'] = smtp_user
        message['To'] = email_address
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [email_address], message.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")

    def view_appointments(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Appointments")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/dashboard.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #menu frame left box
        menu_frame = Frame(self.root, bg="lightgrey")
        menu_frame.place(x=30, y=0, width=300, height=700)

        title = Label(self.root, text="View Appointments", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f").place(x=450, y=30)

        back_icon_image = Image.open("Images/back_icon.png")
        back_icon_resized = back_icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.back_icon = ImageTk.PhotoImage(back_icon_resized)

        self.left_button = tk.Button(self.root, image=self.back_icon, command=self.customer_dashboard, borderwidth=0, highlightthickness=0, bg="white", activebackground="white")
        self.left_button.place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 30, "bold"), bg="lightgrey", fg="black").place(x=100, y=30)


        #book appointment button

        self.book_appointment_button = tk.Label(self.root, text="Book Appointment", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2")
        self.book_appointment_button.pack()
        self.book_appointment_button.bind("<Button-1>", lambda e: self.book_appointment())
        self.book_appointment_button.place(x=75, y=150)
        self.book_appointment_button.bind("<Enter>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="#b89b3f"))
        self.book_appointment_button.bind("<Leave>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="black"))


        #view my appointments button
        self.view_appointments_button = Button(self.root, text="View My Appointments", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black",cursor="hand2", activebackground='lightgrey', command=self.view_appointments)
        self.view_appointments_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_appointments_button.place(x=75, y=200)
        self.view_appointments_button.bind("<Enter>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_appointments_button.bind("<Leave>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg="black"))

        #view services button
        self.view_services_button = Button(self.root, text="View Services", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.view_services_customer)
        self.view_services_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_services_button.place(x=75, y=250)
        self.view_services_button.bind("<Enter>", lambda e: self.view_services_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_services_button.bind("<Leave>", lambda e: self.view_services_button.config(bg="lightgrey", fg="black"))

        #my profile button
        self.my_profile_button = Button(self.root, text="My Profile", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.my_profile)
        self.my_profile_button.config(relief='flat', bd=0, highlightthickness=0)
        self.my_profile_button.place(x=75, y=300)
        self.my_profile_button.bind("<Enter>", lambda e: self.my_profile_button.config(bg="lightgrey", fg='#b89b3f'))
        self.my_profile_button.bind("<Leave>", lambda e: self.my_profile_button.config(bg="lightgrey", fg="black"))

        #logout button
        self.logout_button = Button(self.root, text="Logout", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.login_screen)
        self.logout_button.config(relief='flat', bd=0, highlightthickness=0)
        self.logout_button.place(x=75, y=350)
        self.logout_button.bind("<Enter>", lambda e: self.logout_button.config(bg="lightgrey", fg='#b89b3f'))
        self.logout_button.bind("<Leave>", lambda e: self.logout_button.config(bg="lightgrey", fg="black"))

        #left frame for booking appointment
        left_frame = Frame(self.root, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        

        #table
        self.appointments_table = ttk.Treeview(left_frame, columns=("id", "service", "date", "time", "staff"), selectmode="extended")
        self.appointments_table.heading("id", text="ID")
        self.appointments_table.heading("service", text="Service")
        self.appointments_table.heading("date", text="Date")
        self.appointments_table.heading("time", text="Time")
        self.appointments_table.heading("staff", text="Staff")
        self.appointments_table["show"] = "headings"
        self.appointments_table.column("id", width=3,anchor="center")
        self.appointments_table.column("service", width=50,anchor="center")
        self.appointments_table.column("date", width=30,anchor="center")
        self.appointments_table.column("time", width=30,anchor="center")
        self.appointments_table.column("staff", width=40,anchor="center")
        
        self.appointments_table.tag_configure("oddrow", background="white")
        self.appointments_table.tag_configure("evenrow", background="lightgrey")
        
        self.appointments_table.pack(fill="both", expand=True)

        #fetch data
        mycursor = mydb.cursor()   
        userid=self.userid
        mycursor.execute("SELECT * FROM salon_appointments WHERE customer_id = %s", (userid,))
        rows = mycursor.fetchall()
        for index, row in enumerate(rows):
            service_id = row[2]
            mycursor.execute("SELECT service FROM salon_services WHERE id = %s", (service_id,))
            service = mycursor.fetchone()[0]
            date = row[3]
            time = row[4]

            # convert time
            time = dt.strptime(str(time), "%H:%M:%S").strftime("%I:%M %p")

            # get staff name
            staff_id = row[5]
            # if staff id is not null
            if staff_id != None:
                mycursor.execute("SELECT staffname FROM staff WHERE id = %s", (staff_id,))
                staff = mycursor.fetchone()[0]
            elif row[7] == 1:
                staff = "Checked In"
            else:
                staff = "Not Checked In"

            # insert all data into table
            if index % 2 == 0:
                self.appointments_table.insert("", "end", values=(row[0], service, date, time, staff), tags=("evenrow",))
            else:
                self.appointments_table.insert("", "end", values=(row[0], service, date, time, staff), tags=("oddrow",))

        #checkin appointments button
        self.checkin_appointment_button = Button(left_frame, text="Checkin Appointment", font=("Calibri", 15, "bold"), bg="#b89b3f", fg="white", command=self.checkin_appointment).place(x=95, y=400)
        #cancel appointments button
        self.cancel_appointment_button = Button(left_frame, text="Cancel Appointment", font=("Calibri", 15, "bold"), bg="#b89b3f", fg="white", command=self.cancel_appointment).place(x=100, y=450)

    def checkin_appointment(self):
        #get selected item
        selected_item = self.appointments_table.selection()[0]
        #get id of selected item
        id = self.appointments_table.item(selected_item, "values")[0]
        #update staff id
        mycursor = mydb.cursor()
        #update checkin column
        mycursor.execute("UPDATE salon_appointments SET checkin = 1 WHERE id = %s", (id,))
        mydb.commit()
        messagebox.showinfo("Success", "Checkin Successful")
        self.view_appointments()


    def cancel_appointment(self):
        #get selected item
        selected_item = self.appointments_table.selection()[0]
        #get id of selected item
        id = self.appointments_table.item(selected_item, "values")[0]
        #delete appointment
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM salon_appointments WHERE id = %s", (id,))
        mydb.commit()
        messagebox.showinfo("Success", "Appointment Cancelled")
        self.view_appointments()

    #in customerdashboard user should be able to see services from the salon services table with alternative row in one colour like zebra
    def view_services_customer(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Services")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/dashboard.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #menu frame left box
        menu_frame = Frame(self.root, bg="lightgrey")
        menu_frame.place(x=30, y=0, width=300, height=700)

        title = Label(self.root, text="View Services", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f").place(x=450, y=30)

        back_icon_image = Image.open("Images/back_icon.png")
        back_icon_resized = back_icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.back_icon = ImageTk.PhotoImage(back_icon_resized)

        self.left_button = tk.Button(self.root, image=self.back_icon, command=self.customer_dashboard, borderwidth=0, highlightthickness=0, bg="white", activebackground="white")
        self.left_button.place(x=350, y=30)

        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 30, "bold"), bg="lightgrey", fg="black").place(x=100, y=30)


        #book appointment button

        self.book_appointment_button = tk.Label(self.root, text="Book Appointment", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2")
        self.book_appointment_button.pack()
        self.book_appointment_button.bind("<Button-1>", lambda e: self.book_appointment())
        self.book_appointment_button.place(x=75, y=150)
        self.book_appointment_button.bind("<Enter>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="#b89b3f"))
        self.book_appointment_button.bind("<Leave>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="black"))

        #view my appointments button
        self.view_appointments_button = Button(self.root, text="View My Appointments", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black",cursor="hand2", activebackground='lightgrey', command=self.view_appointments)
        self.view_appointments_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_appointments_button.place(x=75, y=200)
        self.view_appointments_button.bind("<Enter>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_appointments_button.bind("<Leave>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg="black"))

        #view services button
        self.view_services_button = Button(self.root, text="View Services", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.view_services_customer)
        self.view_services_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_services_button.place(x=75, y=250)
        self.view_services_button.bind("<Enter>", lambda e: self.view_services_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_services_button.bind("<Leave>", lambda e: self.view_services_button.config(bg="lightgrey", fg="black"))

        #my profile button
        self.my_profile_button = Button(self.root, text="My Profile", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.my_profile)
        self.my_profile_button.config(relief='flat', bd=0, highlightthickness=0)
        self.my_profile_button.place(x=75, y=300)
        self.my_profile_button.bind("<Enter>", lambda e: self.my_profile_button.config(bg="lightgrey", fg='#b89b3f'))
        self.my_profile_button.bind("<Leave>", lambda e: self.my_profile_button.config(bg="lightgrey", fg="black"))

        #logout button
        self.logout_button = Button(self.root, text="Logout", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.login_screen)
        self.logout_button.config(relief='flat', bd=0, highlightthickness=0)
        self.logout_button.place(x=75, y=350)
        self.logout_button.bind("<Enter>", lambda e: self.logout_button.config(bg="lightgrey", fg='#b89b3f'))
        self.logout_button.bind("<Leave>", lambda e: self.logout_button.config(bg="lightgrey", fg="black"))

        #left frame for booking appointment
        left_frame = Frame(self.root, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #table
        self.services_table = ttk.Treeview(left_frame, columns=("id", "service", "price"), selectmode="extended")
        self.services_table.heading("id", text="ID")
        self.services_table.heading("service", text="Service")
        self.services_table.heading("price", text="Price")
        self.services_table["show"] = "headings"
        self.services_table.column("id", width=5, anchor="center")
        self.services_table.column("service", width=40, anchor="center")
        self.services_table.column("price", width=40, anchor="center")

        self.services_table.pack(fill=BOTH, expand=1)

        # fetch data
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM salon_services")
        rows = mycursor.fetchall()
        for index, row in enumerate(rows):
            if index % 2 == 0:
                self.services_table.insert("", "end", values=(row[0], row[1], row[2]), tags=("even_row",))
            else:
                self.services_table.insert("", "end", values=(row[0], row[1], row[2]), tags=("odd_row",))

        # configure tag colors
        self.services_table.tag_configure("even_row", background="lightgrey")
        self.services_table.tag_configure("odd_row", background="white")

    def my_profile(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - My Profile")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/dashboard.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #menu frame left box
        menu_frame = Frame(self.root, bg="lightgrey")
        menu_frame.place(x=30, y=0, width=300, height=700)

        title = Label(self.root, text="My Profile", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f").place(x=450, y=30)

        back_icon_image = Image.open("Images/back_icon.png")
        back_icon_resized = back_icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.back_icon = ImageTk.PhotoImage(back_icon_resized)

        self.left_button = tk.Button(self.root, image=self.back_icon, command=self.customer_dashboard, borderwidth=0, highlightthickness=0, bg="white", activebackground="white")
        self.left_button.place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 30, "bold"), bg="lightgrey", fg="black").place(x=100, y=30)


        #book appointment button

        self.book_appointment_button = tk.Label(self.root, text="Book Appointment", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2")
        self.book_appointment_button.pack()
        self.book_appointment_button.bind("<Button-1>", lambda e: self.book_appointment())
        self.book_appointment_button.place(x=75, y=150)
        self.book_appointment_button.bind("<Enter>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="#b89b3f"))
        self.book_appointment_button.bind("<Leave>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="black"))


        #view my appointments button
        self.view_appointments_button = Button(self.root, text="View My Appointments", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black",cursor="hand2", activebackground='lightgrey', command=self.view_appointments)
        self.view_appointments_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_appointments_button.place(x=75, y=200)
        self.view_appointments_button.bind("<Enter>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_appointments_button.bind("<Leave>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg="black"))

        #view services button
        self.view_services_button = Button(self.root, text="View Services", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.view_services_customer)
        self.view_services_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_services_button.place(x=75, y=250)
        self.view_services_button.bind("<Enter>", lambda e: self.view_services_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_services_button.bind("<Leave>", lambda e: self.view_services_button.config(bg="lightgrey", fg="black"))

        #my profile button
        self.my_profile_button = Button(self.root, text="My Profile", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.my_profile)
        self.my_profile_button.config(relief='flat', bd=0, highlightthickness=0)
        self.my_profile_button.place(x=75, y=300)
        self.my_profile_button.bind("<Enter>", lambda e: self.my_profile_button.config(bg="lightgrey", fg='#b89b3f'))
        self.my_profile_button.bind("<Leave>", lambda e: self.my_profile_button.config(bg="lightgrey", fg="black"))

        #logout button
        self.logout_button = Button(self.root, text="Logout", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.login_screen)
        self.logout_button.config(relief='flat', bd=0, highlightthickness=0)
        self.logout_button.place(x=75, y=350)
        self.logout_button.bind("<Enter>", lambda e: self.logout_button.config(bg="lightgrey", fg='#b89b3f'))
        self.logout_button.bind("<Leave>", lambda e: self.logout_button.config(bg="lightgrey", fg="black"))


        #left frame for booking appointment
        left_frame = Frame(self.root, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #entry user detials as label and update button
        #get user details
        mycursor = mydb.cursor()
        userid=self.userid
        mycursor.execute("SELECT * FROM customers WHERE id = %s", (userid,))
        user = mycursor.fetchone()
        #print(user)
        #fullname
        self.fullname_label = Label(left_frame, text="First Name:", font=("Calibri", 15, "bold"), bg="white").place(x=50, y=50)
        self.fullname_entry = Label(left_frame, text=user[1], font=("Calibri", 15), bg="white").place(x=180, y=50)

        #lastname
        self.lastname_label = Label(left_frame, text="Last Name:", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=110)
        self.lastname_entry = Label(left_frame, text=user[2], font=("Calibri", 15), bg="white").place(x=170, y=110)

        #email
        self.email_label = Label(left_frame, text="Email:", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=170)
        self.email_entry = Label(left_frame, text=user[3], font=("Calibri", 15), bg="white").place(x=120, y=170)

        #phone
        self.phone_label = Label(left_frame, text="Phone:", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=230)
        self.phone_entry = Label(left_frame, text=user[4], font=("Calibri", 15), bg="white").place(x=120, y=230)

        #username
        self.username_label = Label(left_frame, text="Username:", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=290)
        self.username_entry = Label(left_frame, text=user[5], font=("Calibri", 15), bg="white").place(x=160, y=290)

        #password
        self.password_label = Label(left_frame, text="Password:", font=("Calibri", 15,"bold"), bg="white").place(x=50, y=350)
        self.password_entry = Label(left_frame, text=user[6], font=("Calibri", 15), bg="white").place(x=160, y=350)
        
        #update button
        self.update_button = Button(left_frame, text="Update", font=("Calibri", 15, "bold"), bg="#b89b3f", fg="white", command=self.update_profile).place(x=100, y=420)


    def update_profile(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Update Profile")
        self.root.geometry("1150x700+0+0")

        self.bg_image = Image.open("Images/dashboard.png")  # Update the path to your image
        self.bg_image = self.bg_image.resize((1150, 700), Image.Resampling.LANCZOS)  # Resize the image to fit your screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #menu frame left box
        menu_frame = Frame(self.root, bg="lightgrey")
        menu_frame.place(x=30, y=0, width=300, height=700)

        title = Label(self.root, text="Update Profile", font=("Calibri", 30, "bold"), bg="white", fg="#b89b3f").place(x=450, y=30)

        back_icon_image = Image.open("Images/back_icon.png")
        back_icon_resized = back_icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.back_icon = ImageTk.PhotoImage(back_icon_resized)

        self.left_button = tk.Button(self.root, image=self.back_icon, command=self.my_profile, borderwidth=0, highlightthickness=0, bg="white", activebackground="white")
        self.left_button.place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 30, "bold"), bg="lightgrey", fg="black").place(x=100, y=30)


        #book appointment button

        self.book_appointment_button = tk.Label(self.root, text="Book Appointment", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2")
        self.book_appointment_button.pack()
        self.book_appointment_button.bind("<Button-1>", lambda e: self.book_appointment())
        self.book_appointment_button.place(x=75, y=150)
        self.book_appointment_button.bind("<Enter>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="#b89b3f"))
        self.book_appointment_button.bind("<Leave>", lambda e: self.book_appointment_button.config(bg="lightgrey", fg="black"))


        #view my appointments button
        self.view_appointments_button = Button(self.root, text="View My Appointments", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black",cursor="hand2", activebackground='lightgrey', command=self.view_appointments)
        self.view_appointments_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_appointments_button.place(x=75, y=200)
        self.view_appointments_button.bind("<Enter>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_appointments_button.bind("<Leave>", lambda e: self.view_appointments_button.config(bg="lightgrey", fg="black"))

        #view services button
        self.view_services_button = Button(self.root, text="View Services", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.view_services_customer)
        self.view_services_button.config(relief='flat', bd=0, highlightthickness=0)
        self.view_services_button.place(x=75, y=250)
        self.view_services_button.bind("<Enter>", lambda e: self.view_services_button.config(bg="lightgrey", fg='#b89b3f'))
        self.view_services_button.bind("<Leave>", lambda e: self.view_services_button.config(bg="lightgrey", fg="black"))

        #my profile button
        self.my_profile_button = Button(self.root, text="My Profile", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.my_profile)
        self.my_profile_button.config(relief='flat', bd=0, highlightthickness=0)
        self.my_profile_button.place(x=75, y=300)
        self.my_profile_button.bind("<Enter>", lambda e: self.my_profile_button.config(bg="lightgrey", fg='#b89b3f'))
        self.my_profile_button.bind("<Leave>", lambda e: self.my_profile_button.config(bg="lightgrey", fg="black"))

        #logout button
        self.logout_button = Button(self.root, text="Logout", font=("Calibri", 15, "bold"), bg="lightgrey", fg="black", cursor="hand2", activebackground='lightgrey', command=self.login_screen)
        self.logout_button.config(relief='flat', bd=0, highlightthickness=0)
        self.logout_button.place(x=75, y=350)
        self.logout_button.bind("<Enter>", lambda e: self.logout_button.config(bg="lightgrey", fg='#b89b3f'))
        self.logout_button.bind("<Leave>", lambda e: self.logout_button.config(bg="lightgrey", fg="black"))

        #left frame for booking appointment
        left_frame = Frame(self.root, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #entry user detials as enteries and update button
        #get user details
        mycursor = mydb.cursor()
        userid=self.userid
        mycursor.execute("SELECT * FROM customers WHERE id = %s", (userid,))
        user = mycursor.fetchone()
        #print(user)

        #fullname
        self.fullname_label = Label(left_frame, text="First Name", font=("Calibri", 15), bg="white").place(x=50, y=50)
        self.fullname_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.fullname_entry.insert(0, user[1])
        self.fullname_entry.place(x=50, y=80)

        #lastname
        self.lastname_label = Label(left_frame, text="Last Name", font=("Calibri", 15), bg="white").place(x=50, y=110)
        self.lastname_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.lastname_entry.insert(0, user[2])
        self.lastname_entry.place(x=50, y=140)

        #email
        self.email_label = Label(left_frame, text="Email", font=("Calibri", 15), bg="white").place(x=50, y=170)
        self.email_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.email_entry.insert(0, user[3])
        self.email_entry.place(x=50, y=200)

        #phone
        self.phone_label = Label(left_frame, text="Phone", font=("Calibri", 15), bg="white").place(x=50, y=230)
        self.phone_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.phone_entry.insert(0, user[4])
        self.phone_entry.place(x=50, y=260)

        #username   
        self.username_label = Label(left_frame, text="Username", font=("Calibri", 15), bg="white").place(x=50, y=290)
        self.username_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.username_entry.insert(0, user[5])
        self.username_entry.place(x=50, y=320)

        #password
        self.password_label = Label(left_frame, text="Password", font=("Calibri", 15), bg="white").place(x=50, y=350)
        self.password_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")
        self.password_entry.insert(0, user[6])
        self.password_entry.place(x=50, y=380)

        #update button
        self.update_button = Button(left_frame, text="Save", font=("Calibri", 15, "bold"), bg="#b89b3f", fg="white", command=self.update_profileDB).place(x=100, y=420)

    def update_profileDB(self):
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
                userid=self.userid
                mycursor.execute("UPDATE customers SET firstname = %s, lastname = %s, email = %s, phone = %s, username = %s, password = %s WHERE id = %s", (fullname, lastname, email, phone, username, password, userid))
                mydb.commit()
                messagebox.showinfo("Success", "Profile Updated Successfully", parent=self.root)
                self.customer_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)  





    #admin dashboard
    def admin_dashboard(self):
        #clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Admin Dashboard")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="Admin Dashboard", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)

        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button

        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

    def add_service(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Add Service")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="Add Service", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for adding services
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #service name
        self.service_label = Label(left_frame, text="Service Name", font=("Calibri", 15), bg="white").place(x=50, y=50)
        self.service_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.service_entry.place(x=50, y=80)

        #service price
        self.price_label = Label(left_frame, text="Service Price", font=("Calibri", 15), bg="white").place(x=50, y=110)
        self.price_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.price_entry.place(x=50, y=140)

        #add service button
        self.add_service_button = Button(left_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_serviceDB).place(x=50, y=180)

    def add_serviceDB(self):
        service = self.service_entry.get()
        price = self.price_entry.get()

        if service == "" or price == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("INSERT INTO salon_services (service, price) VALUES (%s, %s)", (service, price))
                mydb.commit()
                messagebox.showinfo("Success", "Service Added Successfully", parent=self.root)
                self.admin_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def view_services(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Services")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="View Services", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for viewing services
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #tree view
        self.services_table = ttk.Treeview(left_frame, columns=("id", "service", "price"), selectmode="extended")
        self.services_table.heading("id", text="ID")
        self.services_table.heading("service", text="Service")
        self.services_table.heading("price", text="Price")

        self.services_table["show"] = "headings"
        self.services_table.column("id", width=5,anchor="center")
        self.services_table.column("service", width=40,anchor="center")
        self.services_table.column("price", width=40,anchor="center")

        self.services_table.pack(fill=BOTH, expand=1)

        #fetch data
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM salon_services")
        rows = mycursor.fetchall()
        for row in rows:
            self.services_table.insert("", "end", values=(row[0], row[1], row[2]))

        #update and delete services
        self.update_service_button = Button(left_frame, text="Update Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.update_service).place(x=50, y=350)
        self.delete_service_button = Button(left_frame, text="Delete Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.delete_service).place(x=250, y=350)

    def update_service(self):
        #get selected item
        selected_item = self.services_table.selection()[0]
        #get id of selected item
        id = self.services_table.item(selected_item, "values")[0]
        #get service name
        service = self.services_table.item(selected_item, "values")[1]
        #get price
        price = self.services_table.item(selected_item, "values")[2]

        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Update Service")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="Update Service", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for updating services
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #service name
        self.service_label = Label(left_frame, text="Service Name", font=("Calibri", 15), bg="white").place(x=50, y=50)
        self.service_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.service_entry.insert(0, service)

        self.service_entry.place(x=50, y=80)

        #service price
        self.price_label = Label(left_frame, text="Service Price", font=("Calibri", 15), bg="white").place(x=50, y=110)
        self.price_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.price_entry.insert(0, price)

        self.price_entry.place(x=50, y=140)

        #update service button
        self.update_service_button = Button(left_frame, text="Update Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=lambda: self.update_serviceDB(id)).place(x=50, y=180)

    def update_serviceDB(self, id):
        service = self.service_entry.get()
        price = self.price_entry.get()

        if service == "" or price == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE salon_services SET service = %s, price = %s WHERE id = %s", (service, price, id))
                mydb.commit()
                messagebox.showinfo("Success", "Service Updated Successfully", parent=self.root)
                self.view_services()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def delete_service(self):
        #get selected item
        selected_item = self.services_table.selection()[0]
        #get id of selected item
        id = self.services_table.item(selected_item, "values")[0]
        #delete service
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM salon_services WHERE id = %s", (id,))
        mydb.commit()
        messagebox.showinfo("Success", "Service Deleted Successfully")
        self.view_services()
    
    def add_staff(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Add Staff")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="Add Staff", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for adding staff
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #staff name
        self.staffname_label = Label(left_frame, text="Staff Name", font=("Calibri", 15), bg="white").place(x=50, y=50)
        self.staffname_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffname_entry.place(x=50, y=80)
        
        #add staff mail
        self.staffmail_label = Label(left_frame, text="Staff Email", font=("Calibri", 15), bg="white").place(x=50, y=110)
        self.staffmail_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffmail_entry.place(x=50, y=140)

        #add staff phone
        self.staffphone_label = Label(left_frame, text="Staff Phone", font=("Calibri", 15), bg="white").place(x=50, y=170)
        self.staffphone_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffphone_entry.place(x=50, y=200)

        #add staff speciality
        self.staffspeciality_label = Label(left_frame, text="Staff Speciality", font=("Calibri", 15), bg="white").place(x=50, y=230)
        self.staffspeciality_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffspeciality_entry.place(x=50, y=260)

        #add staff button
        self.add_staff_button = Button(left_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staffDB).place(x=50, y=300)

    def add_staffDB(self):
        staffname = self.staffname_entry.get()
        staffmail = self.staffmail_entry.get()
        staffphone = self.staffphone_entry.get()
        staffspeciality = self.staffspeciality_entry.get()

        if staffname == "" or staffmail == "" or staffphone == "" or staffspeciality == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("INSERT INTO staff (staffname, staffmail, staffphone, specialization) VALUES (%s, %s, %s, %s)", (staffname, staffmail, staffphone, staffspeciality))
                mydb.commit()
                messagebox.showinfo("Success", "Staff Added Successfully", parent=self.root)
                self.admin_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def view_staff(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Staff")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="View Staff", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg
        ="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for viewing staff
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #tree view
        self.staff_table = ttk.Treeview(left_frame, columns=("id", "name", "email", "phone", "speciality"), selectmode="extended")
        self.staff_table.heading("id", text="ID")
        self.staff_table.heading("name", text="Name")
        self.staff_table.heading("email", text="Email")
        self.staff_table.heading("phone", text="Phone")
        self.staff_table.heading("speciality", text="Speciality")

        self.staff_table["show"] = "headings"
        self.staff_table.column("id", width=5,anchor="center")
        self.staff_table.column("name", width=40,anchor="center")
        self.staff_table.column("email", width=40,anchor="center")
        self.staff_table.column("phone", width=40,anchor="center")
        self.staff_table.column("speciality", width=40,anchor="center")

        self.staff_table.pack(fill=BOTH, expand=1)

        #fetch data
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM staff")
        rows = mycursor.fetchall()

        for row in rows:
            self.staff_table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

        #update and delete staff
        self.update_staff_button = Button(left_frame, text="Update Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.update_staff).place(x=50, y=350)
        self.delete_staff_button = Button(left_frame, text="Delete Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.delete_staff).place(x=250, y=350)

    def update_staff(self):
        #get selected item
        selected_item = self.staff_table.selection()[0]
        #get id of selected item
        id = self.staff_table.item(selected_item, "values")[0]
        #get staff name
        name = self.staff_table.item(selected_item, "values")[1]
        #get email
        email = self.staff_table.item(selected_item, "values")[2]
        #get phone
        phone = self.staff_table.item(selected_item, "values")[3]
        #get speciality
        speciality = self.staff_table.item(selected_item, "values")[4]

        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Update Staff")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="Update Staff", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"),
        bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for updating staff
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #staff name
        self.staffname_label = Label(left_frame, text="Staff Name", font=("Calibri", 15), bg="white").place(x=50, y=50)
        self.staffname_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffname_entry.insert(0, name)

        self.staffname_entry.place(x=50, y=80)

        #staff email
        self.staffmail_label = Label(left_frame, text="Staff Email", font=("Calibri", 15), bg="white").place(x=50, y=110)
        self.staffmail_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffmail_entry.insert(0, email)

        self.staffmail_entry.place(x=50, y=140)

        #staff phone
        self.staffphone_label = Label(left_frame, text="Staff Phone", font=("Calibri", 15), bg="white").place(x=50, y=170)
        self.staffphone_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffphone_entry.insert(0, phone)

        self.staffphone_entry.place(x=50, y=200)

        #staff speciality
        self.staffspeciality_label = Label(left_frame, text="Staff Speciality", font=("Calibri", 15), bg="white").place(x=50, y=230)
        self.staffspeciality_entry = Entry(left_frame, font=("Calibri", 15), bg="#ECECEC")

        self.staffspeciality_entry.insert(0, speciality)

        self.staffspeciality_entry.place(x=50, y=260)

        #update staff button
        self.update_staff_button = Button(left_frame, text="Update Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=lambda: self.update_staffDB(id)).place(x=50, y=300)
        
    def update_staffDB(self, id):
        staffname = self.staffname_entry.get()
        staffmail = self.staffmail_entry.get()
        staffphone = self.staffphone_entry.get()
        staffspeciality = self.staffspeciality_entry.get()

        if staffname == "" or staffmail == "" or staffphone == "" or staffspeciality == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE staff SET staffname = %s, staffmail = %s, staffphone = %s, specialization = %s WHERE id = %s", (staffname, staffmail, staffphone, staffspeciality, id))
                mydb.commit()
                messagebox.showinfo("Success", "Staff Updated Successfully", parent=self.root)
                self.view_staff()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def delete_staff(self):
        #get selected item
        selected_item = self.staff_table.selection()[0]
        #get id of selected item
        id = self.staff_table.item(selected_item, "values")[0]
        #delete staff
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM staff WHERE id = %s", (id,))
        mydb.commit()
        messagebox.showinfo("Success", "Staff Deleted Successfully")
        self.view_staff()

    def view_appointments_admin(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Appointments")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="View Appointments", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #current date label
        current_date = Label(dashboard_frame, text=dt.now().strftime("%m-%d-%Y"), font=("Calibri", 15, "bold"), bg="white", fg="#503D33").place(x=900, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for viewing appointments
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #tree view
        self.appointments_table = ttk.Treeview(left_frame, columns=("id", "name", "email", "phone", "service", "date", "time"), selectmode="extended")
        self.appointments_table.heading("id", text="ID")

        self.appointments_table.heading("name", text="Name")
        self.appointments_table.heading("email", text="Email")
        self.appointments_table.heading("phone", text="Phone")
        self.appointments_table.heading("service", text="Service")
        self.appointments_table.heading("date", text="Date")
        self.appointments_table.heading("time", text="Time")

        self.appointments_table["show"] = "headings"
        self.appointments_table.column("id", width=5,anchor="center")
        self.appointments_table.column("name", width=40,anchor="center")
        self.appointments_table.column("email", width=40,anchor="center")
        self.appointments_table.column("phone", width=40,anchor="center")
        self.appointments_table.column("service", width=40,anchor="center")
        self.appointments_table.column("date", width=40,anchor="center")
        self.appointments_table.column("time", width=40,anchor="center")

        self.appointments_table.pack(fill=BOTH, expand=1)

        #fetch data
        mycursor = mydb.cursor()
        query = "SELECT * FROM salon_appointments WHERE date = CURDATE()"
        mycursor.execute(query)
        rows = mycursor.fetchall()

        if not rows:
            messagebox.showinfo("No Appointments", "No appointments scheduled for today.")
        
        for row in rows:
            Name=row[6]
            userid = row[1]
            email = None
            #get email from database
            mycursor.execute("SELECT email FROM customers WHERE id = %s", (userid,))
            email = mycursor.fetchone()
            email = email[0]
            date=row[3]
            time=str(row[4]) # Convert time to string

            #covert time to HH MM AM/PM
            time = dt.strptime(time, '%H:%M:%S').strftime("%I:%M %p")
            serviceid = row[2]
            service = None
            #get service from database
            mycursor.execute("SELECT service FROM salon_services WHERE id = %s", (serviceid,))
            service = mycursor.fetchone()
            service = service[0]

            #if staff is None, then
            if row[5] == None:
                staffname="Not Available"
            else:
                staffid=row[5]
                staffname = None
                #get staff from database
                mycursor.execute("SELECT staffname FROM staff WHERE id = %s", (staffid,))
                staffname = mycursor.fetchone()
                staffname = staffname[0]

            self.appointments_table.insert("", "end", values=(row[0], Name, email, row[7], service, date, time))

        #assign staff button
        self.assign_staff_button = Button(left_frame, text="Assign Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.assign_staff)
        self.assign_staff_button.place(x=50, y=350)
        
        
        #previous day button
        self.previous_day_button = Button(left_frame, text="Previous Day", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.previous_day)
        self.previous_day_button.place(x=100, y=350)

        #next day button
        self.next_day_button = Button(left_frame, text="Next Day", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.next_day)
        self.next_day_button.place(x=300, y=350)


    # when previous button is clicked the prevoius day appointments are displayed in the table
    def previous_day(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Appointments")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="View Appointments", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #current date label
        current_date = Label(dashboard_frame, text=(dt.now() - timedelta(days=1)).strftime("%m-%d-%Y"), font=("Calibri", 15, "bold"), bg="white", fg="#503D33").place(x=900, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for viewing appointments
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #tree view
        self.appointments_table = ttk.Treeview(left_frame, columns=("id", "name", "email", "phone", "service", "date", "time"), selectmode="extended")
        self.appointments_table.heading("id", text="ID")

        self.appointments_table.heading("name", text="Name")
        self.appointments_table.heading("email", text="Email")
        self.appointments_table.heading("phone", text="Phone")
        self.appointments_table.heading("service", text="Service")
        self.appointments_table.heading("date", text="Date")
        self.appointments_table.heading("time", text="Time")

        self.appointments_table["show"] = "headings"
        self.appointments_table.column("id", width=5,anchor="center")
        self.appointments_table.column("name", width=40,anchor="center")
        self.appointments_table.column("email", width=40,anchor="center")
        self.appointments_table.column("phone", width=40,anchor="center")
        self.appointments_table.column("service", width=40,anchor="center")
        self.appointments_table.column("date", width=40,anchor="center")
        self.appointments_table.column("time", width=40,anchor="center")

        self.appointments_table.pack(fill=BOTH, expand=1)

        #fetch data
        mycursor = mydb.cursor()
        query = "SELECT * FROM salon_appointments WHERE date = CURDATE() - INTERVAL 1 DAY"

        mycursor.execute(query)
        rows = mycursor.fetchall()

        if not rows:
            messagebox.showinfo("No Appointments", "No appointments scheduled for today.")

        for row in rows:
            Name=row[6]
            userid = row[1]
            email = None
            #get email from database
            mycursor.execute("SELECT email FROM customers WHERE id = %s", (userid,))
            email = mycursor.fetchone()
            email = email[0]
            date=row[3]
            time=str(row[4])

            #covert time to HH MM AM/PM
            time = dt.strptime(time, '%H:%M:%S').strftime("%I:%M %p")
            serviceid = row[2]
            service = None
            #get service from database
            mycursor.execute("SELECT service FROM salon_services WHERE id = %s", (serviceid,))
            service = mycursor.fetchone()
            service = service[0]

            #if staff is None, then
            if row[5] == None:
                staffname="Not Available"
            else:
                staffid=row[5]
                staffname = None
                #get staff from database
                mycursor.execute("SELECT staffname FROM staff WHERE id = %s", (staffid,))
                staffname = mycursor.fetchone()
                staffname = staffname[0]

            self.appointments_table.insert("", "end", values=(row[0], Name, email, row[7], service, date, time))
            
        #assign staff button
        self.assign_staff_button = Button(left_frame, text="Assign Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.assign_staff)
        self.assign_staff_button.place(x=50, y=350)

        #previous day button
        self.previous_day_button = Button(left_frame, text="Previous Day", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.previous_day)
        self.previous_day_button.place(x=100, y=350)

        #next day button
        self.next_day_button = Button(left_frame, text="Next Day", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.next_day)
        self.next_day_button.place(x=300, y=350)
   
    
    # when next button is clicked the next day appointments are displayed in the table it should be responsive to the current date
        
        
    def next_day(self):
        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - View Appointments")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="View Appointments", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #current date label
        current_date = Label(dashboard_frame, text=(dt.now() + timedelta(days=1)).strftime("%m-%d-%Y"), font=("Calibri", 15, "bold"), bg="white", fg="#503D33").place(x=900, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_services).place(x=50, y=200)

        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for viewing appointments
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #tree view
        self.appointments_table = ttk.Treeview(left_frame, columns=("id", "name", "email", "phone", "service", "date", "time"), selectmode="extended")
        self.appointments_table.heading("id", text="ID")

        self.appointments_table.heading("name", text="Name")
        self.appointments_table.heading("email", text="Email")
        self.appointments_table.heading("phone", text="Phone")
        self.appointments_table.heading("service", text="Service")
        self.appointments_table.heading("date", text="Date")
        self.appointments_table.heading("time", text="Time")

        self.appointments_table["show"] = "headings"
        self.appointments_table.column("id", width=5,anchor="center")
        self.appointments_table.column("name", width=40,anchor="center")
        self.appointments_table.column("email", width=40,anchor="center")
        self.appointments_table.column("phone", width=40,anchor="center")
        self.appointments_table.column("service", width=40,anchor="center")
        self.appointments_table.column("date", width=40,anchor="center")
        self.appointments_table.column("time", width=40,anchor="center")

        self.appointments_table.pack(fill=BOTH, expand=1)

        #fetch data
        mycursor = mydb.cursor()
        query = "SELECT * FROM salon_appointments WHERE date = CURDATE() + INTERVAL 1 DAY"

        mycursor.execute(query)
        rows = mycursor.fetchall()

        if not rows:
            messagebox.showinfo("No Appointments", "No appointments scheduled for today.")

        for row in rows:
            Name=row[6]
            userid = row[1]
            email = None
            #get email from database
            mycursor.execute("SELECT email FROM customers WHERE id = %s", (userid,))
            email = mycursor.fetchone()
            email = email[0]
            date=row[3]
            time=str(row[4])

            #covert time to HH MM AM/PM
            time = dt.strptime(time, '%H:%M:%S').strftime("%I:%M %p")
            serviceid = row[2]
            service = None
            #get service from database
            mycursor.execute("SELECT service FROM salon_services WHERE id = %s", (serviceid,))
            service = mycursor.fetchone()
            service = service[0]

            #if staff is None, then
            if row[5] == None:
                staffname="Not Available"
            else:
                staffid=row[5]
                staffname = None
                #get staff from database
                mycursor.execute("SELECT staffname FROM staff WHERE id = %s", (staffid,))
                staffname = mycursor.fetchone()
                staffname = staffname[0]

            self.appointments_table.insert("", "end", values=(row[0], Name, email, row[7], service, date, time))

        #assign staff button
        self.assign_staff_button = Button(left_frame, text="Assign Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.assign_staff)
        self.assign_staff_button.place(x=50, y=350)

        #previous day button
        self.previous_day_button = Button(left_frame, text="Previous Day", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.previous_day)
        self.previous_day_button.place(x=100, y=350)

        #next day button
        self.next_day_button = Button(left_frame, text="Next Day", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.next_day)
        self.next_day_button.place(x=300, y=350)


    def assign_staff(self):
        #get selected item
        selected_item = self.appointments_table.selection()[0]
        #get id of selected item
        id = self.appointments_table.item(selected_item, "values")[0]
        #get name
        name = self.appointments_table.item(selected_item, "values")[1]
        #get email
        email = self.appointments_table.item(selected_item, "values")[2]
        #get phone
        phone = self.appointments_table.item(selected_item, "values")[3]
        #get service
        service = self.appointments_table.item(selected_item, "values")[4]
        #get date
        date = self.appointments_table.item(selected_item, "values")[5]
        #get time
        time = self.appointments_table.item(selected_item, "values")[6]

        #same menu section
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Central Salon - Assign Staff")
        self.root.geometry("1150x700+0+0")

        #frame
        dashboard_frame = Frame(self.root, bg="white")
        dashboard_frame.place(x=0, y=0, width=1150, height=700)

        #menu frame left box
        menu_frame = Frame(dashboard_frame, bg="#6D4C3D")
        menu_frame.place(x=30, y=70, width=300, height=400)

        title = Label(dashboard_frame, text="Assign Staff", font=("Calibri", 30, "bold"), bg="white", fg="#503D33").place(x=350, y=30)
        
        #menu label buttons
        self.menu_label = Label(menu_frame, text="Menu", font=("Calibri", 20, "bold"), bg="#6D4C3D", fg="white").place(x=100, y=20)

        #add service button
        self.add_service_button = Button(dashboard_frame, text="Add Service", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_service).place(x=50, y=150)

        #view services button
        self.view_services_button = Button(dashboard_frame, text="View Services", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self
                                           
                                            .view_services).place(x=50, y=200)  
        
        #add staff button
        self.add_staff_button = Button(dashboard_frame, text="Add Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.add_staff).place(x=50, y=250)

        #view staff button
        self.view_staff_button = Button(dashboard_frame, text="View Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_staff).place(x=50, y=300)

        #view appointments button
        self.view_appointments_button = Button(dashboard_frame, text="View Appointments", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.view_appointments_admin).place(x=50, y=350)

        #logout button
        self.logout_button = Button(dashboard_frame, text="Logout", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.login_screen).place(x=50, y=400)

        #left frame for assigning staff
        left_frame = Frame(dashboard_frame, bg="white")
        left_frame.place(x=350, y=100, width=400, height=500)

        #appointment id
        self.appointment_id_label = Label(left_frame, text="Appointment ID:", font=("Calibri", 15, "bold"), bg="white").place(x=50, y=50)
        self.appointment_id_text = Label(left_frame, text=id, font=("Calibri", 15), bg="white")
        self.appointment_id_text.place(x=200, y=50)

        #staff combo box
        self.staff_label = Label(left_frame, text="Staff:", font=("Calibri", 15, "bold"), bg="white").place(x=50, y=110)
        self.staff_combo = ttk.Combobox(left_frame, font=("Calibri", 15))
        self.staff_combo["values"] = ["Select Staff"]

        mycursor = mydb.cursor()
        mycursor.execute("SELECT staffname FROM staff")
        rows = mycursor.fetchall()

        for row in rows:
            self.staff_combo["values"] = self.staff_combo["values"] + (row)

        self.staff_combo.place(x=50, y=140)

        #assign staff button
        self.assign_staff_button = Button(left_frame, text="Assign Staff", font=("Calibri", 15, "bold"), bg="#6D4C3D", fg="white", command=self.assign_staffDB).place(x=50, y=180)

    def assign_staffDB(self):
        appointment_id = self.appointment_id_text.cget("text")
        staff_name = self.staff_combo.get()


        if staff_name == "Select Staff":
            messagebox.showerror("Error", "Please select a staff", parent=self.root)
        else:
            try:
                staffid=None
                mycursor = mydb.cursor()
                mycursor.execute("SELECT id FROM staff WHERE staffname = %s", (staff_name,))
                rows = mycursor.fetchall()
                for row in rows:
                    staffid=row[0]
                mycursor.execute("UPDATE salon_appointments SET staff_id = %s WHERE id = %s", (staffid, appointment_id))
                mydb.commit()
                messagebox.showinfo("Success", "Staff Assigned Successfully", parent=self.root)
                self.view_appointments_admin()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)




#starter code
if __name__ == "__main__":
    root = Tk()
    app = CentralSalon(root)
    icon = PhotoImage(file='Images/central_logo.png')
    root.iconphoto(True, icon)
    root.mainloop()