import hashlib
import tkinter as tk
from tkinter import *

import DBConnection.connectToDB

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()


def forgotUsernameScreen():
    """
    This method creates the tkinter window along with the labels and buttons in the window.
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    window.resizable(False, False)

    username_verify = StringVar()
    email_verify = StringVar()
    password_verify = StringVar()
    confirmPassword_verify = StringVar()

    def verify_password():
        """
        This verifies that the password and email entered exists in the database.
        If it is in the database the user can change their username by adding a new
        username into the entry box on this screen.
        """
        newUsername = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirmPassword = confirm_Password_entry.get()

        t_hashed = hashlib.sha256(password.encode())
        t_password = t_hashed.hexdigest()
        cur.execute("SELECT password, email  FROM Users WHERE password =%s and email = %s",
                    (t_password, email))
        rows = cur.fetchall()
        conn.commit()

        errorLbl = tk.Label(window, text="Credentials are incorrect", font=("Arial", 8), fg="red")
        if rows:
            if password == confirmPassword:
                t_hashed = hashlib.sha256(confirmPassword.encode())
                t_password = t_hashed.hexdigest()
                cur.execute("Update Users set username = %s where password = %s and email=%s",
                            (newUsername, t_password, email))
                conn.commit()
                window.destroy()
            else:
                # Clears the text in the entry box
                username_entry.delete('0', 'end')
                email_entry.delete('0', 'end')
                password_entry.delete('0', 'end')
                confirm_Password_entry.delete('0', 'end')
                errorLbl.place(x=190, y=270)
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            email_entry.delete('0', 'end')
            password_entry.delete('0', 'end')
            confirm_Password_entry.delete('0', 'end')
            errorLbl.place(x=190, y=270)

    def back():
        """
        This method is called when the 'back' button is pressed. The login window is destroyed.
        """
        window.destroy()

    # Creates the GUI elements for buttons and labels
    Label(window, text="").pack()
    Label(window, text="Enter username and new password", font=("Calibri Bold", 18)).pack()
    Label(window, text="").pack()
    Label(window, text="New Username", font=("Calibri", 14)).pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Email", font=("Calibri", 14)).pack()
    email_entry = Entry(window, textvariable=email_verify)
    email_entry.pack()
    Label(window, text="Password", font=("Calibri", 14)).pack()
    password_entry = Entry(window, show="*", textvariable=password_verify)
    password_entry.pack()
    Label(window, text="Confirm Password", font=("Calibri", 14)).pack()
    confirm_Password_entry = Entry(window, show="*", textvariable=confirmPassword_verify)
    confirm_Password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Confirm", width=10, height=1, command=verify_password).place(x=280, y=290)
    Button(window, text="Back", width=10, height=1, command=back).place(x=150, y=290)
