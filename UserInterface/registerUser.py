import tkinter as tk
import UserInterface.FileAccessScreen
from tkinter import *
import UserInterface.InspectorMainScreen


def registerUser():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("300x250")
    window.resizable(False, False)
    username = StringVar()
    password = StringVar()

    def register():
        print("login session started")
        UserInterface.InspectorMainScreen.HomeScreen()

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
    confirm_password_entry = Entry(window, textvariable=password)
    confirm_password_entry.pack()
    Label(window, text="").pack()
    Button(window, text="Register", width=10, height=1, command=register).pack()
    Button(window, text="Back", width=10, height=1, command=back).pack()
