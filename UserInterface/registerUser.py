import tkinter as tk
import UserInterface.FileAccessScreen
from tkinter import *
import UserInterface.InspectorMainScreen
import UserInterface.loginUser


def registerUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250+400+300")
    window.resizable(False, False)
    global username
    global password
    global confirmPassword
    username = StringVar()
    password = StringVar()
    confirmPassword = StringVar()

    def register():
        print("login session started")
        username_info = username_entry.get()
        print("Username: " + username_info)
        password_info = password_entry.get()
        print("Password: " + password_info)
        confirm_password_info = confirm_password_entry.get()
        print("Confirm Password: " + confirm_password_info)

        if password_info != confirm_password_info:
            print("Passwords do not match. Please try again")

        file = open("users.txt", "r+")
        verify = file.read().splitlines()
        if username_info and password_info not in verify:
            print("now")
            file.write(username_info + "\n")
            file.write(password_info + "\n")
            file.close()
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            confirm_password_entry.delete(0, END)
            UserInterface.loginUser.loginUser()
            window.withdraw()
        else:
            print("User with username or password already exists")
        # UserInterface.InspectorMainScreen.HomeScreen()
        # window.withdraw()

    def back():
        window.withdraw()

    Label(window, text="Please enter your details below").pack()
    Label(window, text="").pack()
    Label(window, text="Username").pack()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()
    Label(window, text="Password").pack()
    password_entry = Entry(window, textvariable=password)
    password_entry.pack()
    Label(window, text="Confirm Password").pack()
    confirm_password_entry = Entry(window, textvariable=confirmPassword)
    confirm_password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Register", width=10, height=1, command=register).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
