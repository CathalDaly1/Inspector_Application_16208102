import hashlib
import tkinter as tk
from tkinter import *

from DBConnection import connectToDB

conn = connectToDB.connectToDatabase()
cur = conn.cursor()


def forgotPasswordScreen():
    """ This method creates the tkinter window along with the labels and buttons in the window."""
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    window.resizable(False, False)

    username_verify = StringVar()
    email_verify = StringVar()
    newPassword_verify = StringVar()
    confirmNewPassword_verify = StringVar()

    def changeUsersPassword():
        """
        The data entered into the form is crosschecked with the users previous data in the database
        If the username and email entered in the form is equal to that in the database, their
        new password will be updated and entered into the database.
        """
        username = username_entry.get()
        email = email_entry.get()
        newPassword = newPassword_entry.get()
        confirmNewPassword = confirm_newPassword_entry.get()

        cur.execute("SELECT username, email FROM Users WHERE username =%s and email=%s",
                    (username, email))
        usernameCredentials = cur.fetchall()
        conn.commit()

        errorLbl = tk.Label(window, text="Credentials are incorrect", font=("Calibri", 10), fg="red")
        if usernameCredentials:
            if newPassword == confirmNewPassword:
                t_hashed = hashlib.sha256(confirmNewPassword.encode())
                t_password = t_hashed.hexdigest()
                cur.execute("Update Users set password = %s where username = %s and email=%s",
                            (t_password, username, email))
                conn.commit()
                window.destroy()
            else:
                # Clears the text in the entry box
                username_entry.delete('0', 'end')
                email_entry.delete('0', 'end')
                newPassword_entry.delete('0', 'end')
                confirm_newPassword_entry.delete('0', 'end')
                errorLbl.place(x=180, y=280)
        else:
            username_entry.delete('0', 'end')
            email_entry.delete('0', 'end')
            newPassword_entry.delete('0', 'end')
            confirm_newPassword_entry.delete('0', 'end')
            errorLbl.place(x=180, y=280)

    def back():
        """This method is called when the 'back' button is pressed. The login window is destroyed."""
        window.destroy()

    # Creates the GUI elements for buttons and labels
    Label(window, text="Enter username and new password", font=("Calibri Bold", 18)).pack()
    Label(window, text="").pack()
    Label(window, text="Username", font=("Calibri", 15)).pack()
    username_entry = Entry(window, textvariable=username_verify, font=("Calibri", 13))
    username_entry.pack()
    Label(window, text="Email", font=("Calibri", 15)).pack()
    email_entry = Entry(window, textvariable=email_verify, font=("Calibri", 13))
    email_entry.pack()
    Label(window, text="New Password", font=("Calibri", 15)).pack()
    newPassword_entry = Entry(window, show="*", textvariable=newPassword_verify, font=("Calibri", 13))
    newPassword_entry.pack()
    Label(window, text="Confirm New Password", font=("Calibri", 15)).pack()
    confirm_newPassword_entry = Entry(window, show="*", textvariable=confirmNewPassword_verify, font=("Calibri", 13))
    confirm_newPassword_entry.pack()
    Label(window, text="").pack()
    confirmButton = Button(window, text="Confirm", width=10, height=1, command=changeUsersPassword, font=("Calibri", 12))
    confirmButton.place(x=280, y=305)
    backButton = Button(window, text="Back", width=10, height=1, command=back, font=("Calibri", 12))
    backButton.place(x=150, y=305)
