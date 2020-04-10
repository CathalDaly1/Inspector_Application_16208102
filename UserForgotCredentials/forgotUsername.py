import hashlib
import tkinter as tk
from tkinter import *
import DBConnection.connectToDB

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()


def forgotUsernameScreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    window.resizable(False, False)

    username_verify = StringVar()
    password_verify = StringVar()
    confirmPassword_verify = StringVar()

    def verify_password():
        newUsername = username_entry.get()
        password = password_entry.get()
        confirmPassword = confirm_Password_entry.get()

        t_hashed = hashlib.sha256(password.encode())
        t_password = t_hashed.hexdigest()
        cur.execute("SELECT password  FROM Users WHERE password =%s",
                    (t_password,))
        rows = cur.fetchall()
        conn.commit()

        errorLbl = tk.Label(window, text="Credentials are incorrect", font=("Arial", 8), fg="red")
        if rows:
            for row in rows:
                if password == confirmPassword and t_password == row[0]:
                    t_hashed = hashlib.sha256(confirmPassword.encode())
                    t_password = t_hashed.hexdigest()
                    cur.execute("Update Users set username = %s where password = %s",
                                (newUsername, t_password,))
                    conn.commit()
                    window.destroy()
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            password_entry.delete('0', 'end')
            confirm_Password_entry.delete('0', 'end')
            errorLbl.place(x=190, y=220)

    def back():
        window.destroy()

    # Creates the GUI elements for buttons and labels
    Label(window, text="").pack()
    Label(window, text="Enter username and new password", font=("Calibri Bold", 18)).pack()
    Label(window, text="").pack()
    Label(window, text="New Username", font=("Calibri", 14)).pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Password", font=("Calibri", 14)).pack()
    password_entry = Entry(window, show="*", textvariable=password_verify)
    password_entry.pack()
    Label(window, text="Confirm Password", font=("Calibri", 14)).pack()
    confirm_Password_entry = Entry(window, show="*", textvariable=confirmPassword_verify)
    confirm_Password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Confirm", width=10, height=1, command=verify_password).place(x=280, y=240)
    Button(window, text="Back", width=10, height=1, command=back).place(x=150, y=240)
