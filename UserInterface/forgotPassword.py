import hashlib
import tkinter as tk
from tkinter import *

# Connects to the database
# ToDo Place this into one file and instantiate into the REST API
import psycopg2


def connectToDB():
    connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Cannot connect to the DB")


conn = connectToDB()
cur = conn.cursor()


def forgotPasswordScreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250+400+300")
    window.resizable(False, False)

    username_verify = StringVar()
    newPassword_verify = StringVar()
    confirmNewPassword_verify = StringVar()

    def verify_username():
        username1 = username_entry.get()
        newPassword = newPassword_entry.get()
        confirmNewPassword = confirm_newPassword_entry.get()

        cur.execute("SELECT username  FROM Users WHERE username =%s",
                    (username1,))
        rows = cur.fetchall()

        errorLbl = tk.Label(window, text="Credentials are incorrect", font=("Arial", 8), fg="red")
        if rows:
            for row in rows:
                if username1 == row[0]:
                    t_hashed = hashlib.sha256(confirmNewPassword.encode())
                    t_password = t_hashed.hexdigest()
                    cur.execute("Update Users set password = %s where username = %s",
                                (t_password, username1,))
                    conn.commit()
                    window.destroy()
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            errorLbl.place(x=80, y=180)

    def back():
        window.destroy()

    # Creates the GUI elements for buttons and labels
    Label(window, text="Enter username and new password", font=("Calibri Bold", 14)).pack()
    Label(window, text="").pack()
    Label(window, text="Username", font=("Calibri", 12)).pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="New Password", font=("Calibri", 12)).pack()
    newPassword_entry = Entry(window, show="*", textvariable=newPassword_verify)
    newPassword_entry.pack()
    Label(window, text="Confirm New Password", font=("Calibri", 12)).pack()
    confirm_newPassword_entry = Entry(window, show="*", textvariable=confirmNewPassword_verify)
    confirm_newPassword_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Confirm", width=10, height=1, command=verify_username).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
