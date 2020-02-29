import tkinter as tk

import psycopg2
import bcrypt

import UserInterface.FileAccessScreen
from tkinter import *
import UserInterface.InspectorMainScreen
import UserInterface.loginUser
import RestAPI.db


# Created the GUI Screen and also stores each method used in this window
# Global variables are used in order to reach all methods in this class
def registerUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250+400+300")
    window.resizable(False, False)
    global username
    global password
    global confirmPassword
    username = StringVar()
    password = StringVar()
    confirmPassword = StringVar()

# Register user connects the the PostgreSQL database, checks connection
    def register():
        def connectToDB():
            connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
            try:
                return psycopg2.connect(connectionString)
            except:
                print("Cannot connect to the DB")

        conn = connectToDB()
        cur = conn.cursor()

        # Once connected gets the username and password in the entry boxes in GUI
        print("login session started")
        username_info = username_entry.get()
        password_info = password_entry.get()
        confirm_password_info = confirm_password_entry.get()

        # Error handling: checks if the fields have been filled out
        # Inserts username and password into the database - also uid is inserted
        if username_info and password_info != "":
            # Error handling checks if password and confirm password are identical
            if password_info != confirm_password_info:
                errorLbl = tk.Label(window, text="Passwords do not match", font=("Arial", 8), fg="red")
                errorLbl.place(x=100, y=165)

            else:
                sql = "INSERT INTO Users (username, password) VALUES (%s, %s)"
                val = (username_info, password_info)
                # Executes the insertion ans passes values username and password into the insertion
                cur.execute(sql, val)
                # Closes the connection to the database
                conn.commit()
                window.withdraw()
                UserInterface.loginUser.loginUser()
        else:
            # If password and confirm passord are now the same, display error message
            errorLbl2 = tk.Label(window, text="Please fill in all fields", font=("Arial", 8), fg="red")
            errorLbl2.place(x=100, y=165)

    def back():
        window.withdraw()

    # Creates the GUI elements for buttons and labels
    Label(window, text="Please enter your details below").pack()
    Label(window, text="").pack()
    Label(window, text="Username").pack()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()
    Label(window, text="Password").pack()
    password_entry = Entry(window, show="*", textvariable=password)
    password_entry.pack()
    Label(window, text="Confirm Password").pack()
    confirm_password_entry = Entry(window, show="*", textvariable=confirmPassword)
    confirm_password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Register", width=10, height=1, command=register).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
