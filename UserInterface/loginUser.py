import tkinter as tk

import psycopg2

import UserInterface.FileAccessScreen
from tkinter import *
import os
import UserInterface.InspectorMainScreen


def loginUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250+400+300")
    window.resizable(False, False)

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

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

    def login():
        print("login session started")
        UserInterface.InspectorMainScreen.HomeScreen()
        window.withdraw()

    def back():
        window.withdraw()

    def login_verify():
        username1 = username_entry.get()
        password1 = password_entry.get()
        cur.execute("SELECT username, password  FROM Users WHERE username =%s and password =%s", (username1, password1,))
        rows = cur.fetchall()

        # Check if returned set is not empty: checks if data is correct
        if rows:
            for row in rows:
                if username1 == row[0] or password1 == row[1]:
                    login()
        else:
            errorLbl = tk.Label(window, text="Incorrect Username or password", font=("Arial", 8), fg="red")
            errorLbl.place(x=60, y=125)

    Label(window, text="Please enter your details below").pack()
    Label(window, text="").pack()
    Label(window, text="Username").pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Password").pack()
    password_entry = Entry(window, textvariable=password_verify)
    password_entry.pack()
    Label(window, text="\n").pack()
    Button(window, text="Login", width=10, height=1, command=login_verify).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
