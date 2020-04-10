from tkinter import *
import tkinter as tk
import UserCredentials.loginUser
import UserCredentials.registerUser


class UserMainScreen(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,
                         default='C:/Users/catha/PycharmProjects/Inspector_Application/InspectorFavicon/Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.geometry("500x350+400+300")
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
    UserCredentials.loginUser.LoginUser()


# Calls login method from the RegisterUser class
def register():
    UserCredentials.registerUser.registerUser()


# Class to create a user, setup here is the GUI
class create_account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # create a Form label
        Label(self, text="Inspector - Grading Application", bg="grey", width="300", height="2",
              font=("Bold", 22)).pack()
        Label(self, text="").pack()

        Label(self, text="Register or Login below", width="300", height="2",
              font=("Bold", 20)).pack()

        # create Login Button
        Label(self, text="").pack()
        loginButton = Button(self, text="Login", command=login, width=10, height=1, font="Bold", borderwidth=3)
        loginButton.pack()
        Label(self, text="").pack()
        # create a register button
        registerButton = Button(self, text="Register", command=register, width=10, height=1, font="Bold", borderwidth=3)
        registerButton.pack()


# Run files
if __name__ == "__main__":
    app = UserMainScreen()
    app.mainloop()
