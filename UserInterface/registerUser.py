import tkinter as tk

import psycopg2

import UserInterface.FileAccessScreen
from tkinter import *
import UserInterface.InspectorMainScreen
import UserInterface.loginUser


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

    def register():
        def connectToDB():
            connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
            print(connectionString)
            try:
                print("Connected successfully")
                return psycopg2.connect(connectionString)
            except:
                print("Cannot connect to the DB")

        conn = connectToDB()
        cur = conn.cursor()

        print("login session started")
        username_info = username_entry.get()
        print("Username: " + username_info)
        password_info = password_entry.get()
        print("Password: " + password_info)
        confirm_password_info = confirm_password_entry.get()
        print("Confirm Password: " + confirm_password_info)

        if username_info and password_info != "":
            if password_info != confirm_password_info:
                errorLbl = tk.Label(window, text="Passwords do not match", font=("Arial", 8), fg="red")
                errorLbl.place(x=100, y=165)

            else:
                sql = "INSERT INTO Users (username, password) VALUES (%s, %s)"
                val = (username_info, password_info)
                cur.execute(sql, val)
                conn.commit()
                window.withdraw()
                UserInterface.loginUser.loginUser()
        else:
            errorLbl2 = tk.Label(window, text="Please fill in all fields", font=("Arial", 8), fg="red")
            errorLbl2.place(x=100, y=165)

        # Check if returned set is not empty: checks if data is correct

    def back():
        window.withdraw()

    Label(window, text="Please enter your details below").pack()
    Label(window, text="").pack()
    Label(window, text="Username").pack()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()
    Label(window, text="Password").pack()
    password_entry = Entry(window, textvariable=password)
    password_entry.pack()
    Label(window, text="Confirm Password").pack()
    confirm_password_entry = Entry(window, textvariable=confirmPassword)
    confirm_password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Register", width=10, height=1, command=register).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
