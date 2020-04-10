import hashlib
import tkinter as tk
from tkinter import *

import DBConnection.connectToDB
import UserCredentials.loginUser


# Created the GUI Screen and also stores each method used in this window
# Global variables are used in order to reach all methods in this class
def registerUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    window.resizable(False, False)
    global username
    global password
    global confirmPassword
    username = StringVar()
    password = StringVar()
    email = StringVar()
    confirmPassword = StringVar()

    # Register user connects the the PostgreSQL database, checks connection
    def register():

        conn = DBConnection.connectToDB.connectToDB()
        cur = conn.cursor()

        # Once connected gets the username and password in the entry boxes in GUI
        username_info = username_entry.get()
        email_info = email_entry.get()
        password_info = password_entry.get()
        confirm_password_info = confirm_password_entry.get()

        # Error handling: checks if the fields have been filled out
        # Inserts username and password into the database - also uid is inserted
        if username_info and email_info and password_info != "":
            # Error handling checks if password and confirm password are identical
            if password_info != confirm_password_info:
                errorLbl = tk.Label(window, text="Passwords do not match", font=("Arial", 8), fg="red")
                errorLbl.place(x=90, y=185)

            else:
                # Hashing the users password and inserting into the database
                t_hashed = hashlib.sha256(password_info.encode())
                t_password = t_hashed.hexdigest()
                insertUser = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
                val = (username_info, email_info, t_password)
                # Executes the insertion ans passes values username and password into the insertion
                cur.execute(insertUser, val)
                # Closes the connection to the database
                conn.commit()

                window.withdraw()
                UserCredentials.loginUser.LoginUser()
        else:
            # If password and confirm password are not the same, display error message
            errorLbl2 = tk.Label(window, text="Please fill in all fields", font=("Arial", 8), fg="red")
            errorLbl2.place(x=200, y=247)

    def back():
        window.withdraw()

    # Creates the GUI elements for buttons and labels
    Label(window, text="").pack()
    Label(window, text="Please enter your credentials below", font=("Bold", 18)).pack()
    Label(window, text="Username", font=("Calibri", 14)).pack()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()
    Label(window, text="Email", font=("Calibri", 14)).pack()
    email_entry = Entry(window, textvariable=email)
    email_entry.pack()
    Label(window, text="Password", font=("Calibri", 14)).pack()
    password_entry = Entry(window, show="*", textvariable=password)
    password_entry.pack()
    Label(window, text="Confirm Password", font=("Calibri", 14)).pack()
    confirm_password_entry = Entry(window, show="*", textvariable=confirmPassword)
    confirm_password_entry.pack()
    Button(window, text="Register", width=10, height=1, command=register, borderwidth=3).place(x=280, y=270)
    Button(window, text="Back", width=10, height=1, command=back, borderwidth=3).place(x=150, y=270)
