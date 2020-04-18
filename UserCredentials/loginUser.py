import datetime
import hashlib
import tkinter as tk
from tkinter import *

import DBConnection.connectToDB
import HomeScreen.InspectorHomescreen
import ChangingUsersCredentials.forgotPassword
import ChangingUsersCredentials.forgotUsername

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()

parameters = {
    "username": "test"
}


# response = requests.get("http://localhost:5000/userInfo/")
# print(response.status_code)
# print(response.json())


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
        global username1, time_logged_in

        # username = request.form['username']
        # print(username)

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
                    HomeScreen.InspectorHomescreen.Homescreen()
                    window.destroy()
        else:
            # Clears the text in the entry box
            username_entry.delete('0', 'end')
            password_entry.delete('0', 'end')
            errorLbl.place(x=170, y=170)

    def callbackPassword(event):
        """
        This method is called when the 'forgot password' hyperlink is clicked. User is directed to the
        forgot password screen.
        :param event:
        """
        ChangingUsersCredentials.forgotPassword.forgotPasswordScreen()

    def callbackUsername(event):
        """
        This method is called when the 'forgot username' hyperlink is clicked. User is directed to the
        forgot username screen.
        :param event:
        """
        ChangingUsersCredentials.forgotUsername.forgotUsernameScreen()

    Label(window, text="").pack()
    Label(window, text="Please enter your credentials below", font=("Bold", 18)).pack()
    Label(window, text="").pack()
    Label(window, text="Username", font=("Calibri", 14)).pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Password", font=("Calibri", 14)).pack()
    password_entry = Entry(window, show="*", textvariable=password_verify)
    password_entry.pack()
    lblUsername = tk.Label(window, text=r"Forgot Username?", fg="blue", cursor="hand2")
    lblUsername.place(x=200, y=190)
    lblUsername.bind("<Button-1>", callbackUsername)
    lblPassword = tk.Label(window, text=r"Forgot Password?", fg="blue", cursor="hand2")
    lblPassword.place(x=200, y=210)
    lblPassword.bind("<Button-1>", callbackPassword)
    loginButton = Button(window, text="Login", width=10, height=1, command=login_verify, borderwidth=3)
    loginButton.place(x=280, y=240)
    backButton = Button(window, text="Back", width=10, height=1, command=back, borderwidth=3)
    backButton.place(x=150, y=240)


def getUserID():
    """
    This method is used to get the users ID number from the users database table.
    :return:
    """
    cur.execute("SELECT uid::int FROM USERS WHERE username =%s",
                (username1,))
    uid = cur.fetchone()
    conn.commit()
    userUID = int(uid[0])
    return userUID


def getUsername():
    """
    This method returns the username that has been retrieved from the login form.
    :return:
    """
    return username1


def getTimeLoggedIn():
    """
    This method returns the user time when they logged in.
    :return:
    """
    return time_logged_in
