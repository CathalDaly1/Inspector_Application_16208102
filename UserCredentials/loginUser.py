import datetime
import hashlib
import tkinter as tk
from tkinter import *

from DBConnection import connectToDB
from HomeScreen import InspectorHomescreen
from ChangingUsersCredentials import forgotPassword, forgotUsername

conn = connectToDB.connectToDatabase()
cur = conn.cursor()


def LoginUser():
    """
    This method creates the tkinter window along with the labels and buttons in the window.
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("500x350+400+300")
    username_verify = StringVar()
    password_verify = StringVar()

    def back():
        """
        This method is called when the 'back' button is pressed. The login window is destroyed.
        """
        window.withdraw()

    def login_verify():
        """
        This method checks if the username and password entered are in the database.
        """
        global username, time_logged_in

        # Get the text which has been entered into the entry area
        username = username_entry.get()
        password1 = password_entry.get()
        # Retrieving the users hashed password
        t_hashed = hashlib.sha256(password1.encode())
        t_password = t_hashed.hexdigest()
        # Executes a select statement which verify's if username and password are in DB
        cur.execute("SELECT username, password  FROM Users WHERE username =%s and password =%s",
                    (username, t_password,))
        rows = cur.fetchall()
        conn.commit()

        time_logged_in = datetime.datetime.now()

        # Check if there is data in the database
        # Loops through the username's and passwords
        # Creates a set of [Username, password] and checks if they match
        errorLbl = tk.Label(window, text="Incorrect Username or password", font=("Calibri", 10), fg="red")
        if rows:
            for row in rows:
                if username == row[0] and t_password == row[1]:
                    InspectorHomescreen.Homescreen()
                    window.destroy()
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            password_entry.delete('0', 'end')
            errorLbl.place(x=158, y=190)

    def callbackPassword(event):
        """
        This method is called when the 'forgot password' hyperlink is clicked. User is directed to the
        forgot password screen.
        :param event:
        """
        forgotPassword.forgotPasswordScreen()

    def callbackUsername(event):
        """
        This method is called when the 'forgot username' hyperlink is clicked. User is directed to the
        forgot username screen.
        :param event:
        """
        forgotUsername.forgotUsernameScreen()

    Label(window, text="").pack()
    Label(window, text="Please enter your credentials below", font=("Calibri Bold", 18)).pack()
    Label(window, text="").pack()
    Label(window, text="Username", font=("Calibri", 15)).pack()
    username_entry = Entry(window, textvariable=username_verify, font=("Calibri", 13))
    username_entry.pack()
    Label(window, text="Password", font=("Calibri", 15)).pack()
    password_entry = Entry(window, show="*", textvariable=password_verify, font=("Calibri", 13))
    password_entry.pack()
    lblUsername = tk.Label(window, text=r"Forgot Username?", fg="blue", cursor="hand2", font=("Calibri", 11))
    lblUsername.place(x=190, y=210)
    lblUsername.bind("<Button-1>", callbackUsername)
    lblPassword = tk.Label(window, text=r"Forgot Password?", fg="blue", cursor="hand2", font=("Calibri", 11))
    lblPassword.place(x=190, y=230)
    lblPassword.bind("<Button-1>", callbackPassword)
    loginButton = Button(window, text="Login", width=10, height=1, command=login_verify, font=("Calibri", 12), borderwidth=3)
    loginButton.place(x=280, y=260)
    backButton = Button(window, text="Back", width=10, height=1, command=back, font=("Calibri", 12), borderwidth=3)
    backButton.place(x=140, y=260)


def getUserID():
    """
    This method is used to get the users ID number from the users database table.
    :return:
    """
    cur.execute("SELECT uid::int FROM USERS WHERE username =%s",
                (username,))
    uid = cur.fetchone()
    conn.commit()
    userUID = int(uid[0])
    return userUID


def getUsername():
    """
    This method returns the username that has been retrieved from the login form.
    :return:
    """
    return username


def getTimeLoggedIn():
    """
    This method returns the user time when they logged in.
    :return:
    """
    return time_logged_in
