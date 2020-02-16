import tkinter as tk
import UserInterface.FileAccessScreen
from tkinter import *
import os
import UserInterface.InspectorMainScreen


def loginUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250+400+300")
    window.resizable(False, False)

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    def login():
        print("login session started")
        UserInterface.InspectorMainScreen.HomeScreen()
        window.withdraw()

    def back():
        window.withdraw()

    def login_verify():
        username1 = username_verify.get()
        password1 = password_entry.get()
        print("getting this far")
        print(password1)
        path = "C:/Users/catha/PycharmProjects/Inspector_Application/UserInterface"
        list_of_files = os.listdir(path)
        if "users.txt" in list_of_files:
            file1 = open("users.txt", "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                login()
            else:
                print("User is not on the system")

    Label(window, text="Please enter your details below").pack()
    Label(window, text="").pack()
    Label(window, text="Username").pack()
    username_entry = Entry(window, textvariable=username_verify)
    username_entry.pack()
    Label(window, text="Password").pack()
    password_entry = Entry(window, textvariable=password_verify)
    password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Login", width=10, height=1, command=login_verify).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
