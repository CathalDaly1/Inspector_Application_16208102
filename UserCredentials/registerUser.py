import hashlib
import tkinter as tk
from tkinter import *

import DBConnection.connectToDB
import UserCredentials.loginUser

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()


def registerUser():
    """
    This method creates the tkinter window along with the labels and buttons in the window.
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    window.resizable(False, False)

    username = StringVar()
    password = StringVar()
    email = StringVar()
    confirmPassword = StringVar()

    def register():
        """
        This method verifies that the username, password and confirmation password are identical.
        The user is then registered. The credentials are entered in the database and the user
        can then access the application using their credentials.
        """
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
                usersValues = (username_info, email_info, t_password)
                # Executes the insertion ans passes values username and password into the insertion
                cur.execute(insertUser, usersValues)
                # Closes the connection to the database
                conn.commit()

                window.withdraw()
                UserCredentials.loginUser.LoginUser()
        else:
            # If password and confirm password are not the same, display error message
            errorLbl2 = tk.Label(window, text="Please fill in all fields", font=("Arial", 8), fg="red")
            errorLbl2.place(x=200, y=247)

    def back():
        """
        This method is called when the 'back' button is pressed. The login window is destroyed.
        """
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
