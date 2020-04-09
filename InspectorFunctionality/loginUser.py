import datetime
import hashlib
import tkinter as tk
from tkinter import *

import InspectorFunctionality.FileAccessScreen
import InspectorFunctionality.LoginRegScreen
import InspectorFunctionality.connectToDB
import InspectorFunctionality.forgotPassword
import InspectorFunctionality.forgotUsername
import InspectorFunctionality.InspectorHomescreen

conn = InspectorFunctionality.connectToDB.connectToDB()
cur = conn.cursor()


def LoginUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250+400+300")

    username_verify = StringVar()
    password_verify = StringVar()

    def back():
        window.withdraw()

    # Checks if the username and password are in the database
    def login_verify():
        global username1
        global time_logged_in

        # Get the text which has been entered into the entry area
        username1 = username_entry.get()
        password1 = password_entry.get()
        # Retrieving the users hashed password
        t_hashed = hashlib.sha256(password1.encode())
        t_password = t_hashed.hexdigest()
        # Executes a select statement which verify's if username and password are in DB
        cur.execute("SELECT username, password  FROM Users WHERE username =%s and password =%s",
                    (username1, t_password,))
        rows = cur.fetchall()
        conn.commit()

        time_logged_in = datetime.datetime.now()

        # Check if there is data in the database
        # Loops through the username's and passwords
        # Creates a set of [Username, password] and checks if they match
        errorLbl = tk.Label(window, text="Incorrect Username or password", font=("Arial", 8), fg="red")
        if rows:
            for row in rows:
                if username1 == row[0] and t_password == row[1]:
                    InspectorFunctionality.InspectorHomescreen.Homescreen()
                    window.destroy()
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            password_entry.delete('0', 'end')
            errorLbl.place(x=60, y=180)

    def callbackPassword(event):
        InspectorFunctionality.forgotPassword.forgotPasswordScreen()

    def callbackUsername(event):
        InspectorFunctionality.forgotUsername.forgotUsernameScreen()

    Label(window, text="Please enter your credentials below", font=("Calibri Bold", 14)).pack()
    Label(window, text="").pack()
    Label(window, text="Username", font=("Calibri", 12)).pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Password", font=("Calibri", 12)).pack()
    password_entry = Entry(window, show="*", textvariable=password_verify)
    password_entry.pack()
    Label(window, text="\n").pack()
    lblUsername = tk.Label(window, text=r"Forgot Username?", fg="blue", cursor="hand2")
    lblUsername.place(x=100, y=140)
    lblUsername.bind("<Button-1>", callbackUsername)
    lblPassword = tk.Label(window, text=r"Forgot Password?", fg="blue", cursor="hand2")
    lblPassword.place(x=100, y=160)
    lblPassword.bind("<Button-1>", callbackPassword)
    loginButton = Button(window, text="Login", width=10, height=1, command=login_verify)
    loginButton.place(x=110, y=199)
    backButton = Button(window, text="Back", width=10, height=1, command=back)
    backButton.place(x=110, y=225)


def getUserID():
    cur.execute("SELECT uid::int FROM USERS WHERE username =%s",
                (username1,))
    uid = cur.fetchone()
    conn.commit()
    userUID = int(uid[0])
    return userUID


def getUsername():
    return username1


def getTimeLoggedIn():
    return time_logged_in
