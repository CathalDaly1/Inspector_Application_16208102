from tkinter import *
import tkinter as tk
import UserInterface.loginUser
import UserInterface.registerUser

class UserMainScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.geometry("300x250")
        self.title("Inspector - Grading Application")
        self.resizable(False, False)

        frame = create_account(container, self)
        self.frames[create_account] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(create_account)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def login():
    print("login button clicked")
    UserInterface.loginUser.loginUser()


def register():
    print("register button clicked")
    UserInterface.registerUser.registerUser()


class create_account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create a Form label
        Label(self, text="Choose Login Or Register", bg="grey", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()

        # create Login Button
        loginButton = Button(self, text="Login", command=login, height=1, width=6)
        Label(text="").pack()
        loginButton.pack()
        Label(text="").pack()

        # create a register button
        Label(text="").pack()
        registerButton = Button(self, text="Register", command=register, height=1, width=6)
        registerButton.pack()


if __name__ == "__main__":
    app = UserMainScreen()
    app.mainloop()
