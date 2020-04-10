import hashlib
import tkinter as tk
from tkinter import *
import DBConnection.connectToDB

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()


def forgotPasswordScreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    window.resizable(False, False)

    username_verify = StringVar()
    email_verify = StringVar()
    newPassword_verify = StringVar()
    confirmNewPassword_verify = StringVar()

    def verify_username():
        username1 = username_entry.get()
        email = email_entry.get()
        newPassword = newPassword_entry.get()
        confirmNewPassword = confirm_newPassword_entry.get()

        cur.execute("SELECT username, email FROM Users WHERE username =%s and email=%s",
                    (username1, email))
        usernameCred = cur.fetchall()
        conn.commit()

        errorLbl = tk.Label(window, text="Credentials are incorrect", font=("Arial", 8), fg="red")
        if usernameCred:
            for row in usernameCred:
                if username1 == row[0] and newPassword == confirmNewPassword:
                    t_hashed = hashlib.sha256(confirmNewPassword.encode())
                    t_password = t_hashed.hexdigest()
                    cur.execute("Update Users set password = %s where username = %s and email=%s",
                                (t_password, username1, email))
                    conn.commit()
                    window.destroy()
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            newPassword_entry.delete('0', 'end')
            confirm_newPassword_entry.delete('0', 'end')
            errorLbl.place(x=190, y=270)

    def back():
        window.destroy()

    # Creates the GUI elements for buttons and labels
    Label(window, text="").pack()
    Label(window, text="Enter username and new password", font=("Bold", 18)).pack()
    Label(window, text="").pack()
    Label(window, text="Username", font=("Calibri", 14)).pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Email", font=("Calibri", 14)).pack()
    email_entry = Entry(window, textvariable=email_verify)
    email_entry.pack()
    Label(window, text="New Password", font=("Calibri", 14)).pack()
    newPassword_entry = Entry(window, show="*", textvariable=newPassword_verify)
    newPassword_entry.pack()
    Label(window, text="Confirm New Password", font=("Calibri", 14)).pack()
    confirm_newPassword_entry = Entry(window, show="*", textvariable=confirmNewPassword_verify)
    confirm_newPassword_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Confirm", width=10, height=1, command=verify_username).place(x=280, y=290)
    Button(window, text="Back", width=10, height=1, command=back).place(x=150, y=290)
