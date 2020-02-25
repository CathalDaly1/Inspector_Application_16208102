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
        self.geometry("300x250+400+300")
        self.title("Inspector - Grading Application")
        self.resizable(False, False)

        frame = create_account(container, self)
        self.frames[create_account] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(create_account)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Calls login method from the LoginUser class
def login():
    print("login button clicked")
    UserInterface.loginUser.loginUser()


# Calls login method from the RegisterUser class
def register():
    print("register button clicked")
    UserInterface.registerUser.registerUser()


# Class to create a user, setup here is the GUI
class create_account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create a Form label
        Label(self, text="Choose Login Or Register", bg="grey", width="300", height="2", font=("Calibri", 13)).pack()
        Label(self, text="").pack()

        # create Login Button
        loginButton = Button(self, text="Login", command=login, width=10, height=1)
        Label(self, text="").pack()
        loginButton.pack()
        Label(self, text="").pack()

        # create a register button
        registerButton = Button(self, text="Register", command=register, width=10, height=1)
        registerButton.pack()


# Run files
if __name__ == "__main__":
    app = UserMainScreen()
    app.mainloop()
