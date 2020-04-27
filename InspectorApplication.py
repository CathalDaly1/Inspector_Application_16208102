import tkinter as tk
from tkinter import *

from UserCredentials import loginUser, registerUser


class UserMainScreen(tk.Tk):
    """ This method creates the tkinter frame and window along with the elements of the tkinter window. """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default='C:/Users/catha/PycharmProjects/Inspector_Application/Inspector.ico')

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
        """
        This method initializes the frame
        :param cont:
        """
        frame = self.frames[cont]
        frame.tkraise()


def login():
    """
    This method is called when the 'login' button is pressed. Directs the user to the login screen.
    """
    loginUser.LoginUser()


# Calls login method from the RegisterUser class
def register():
    """
    This method is called when the 'register' button is pressed. Directs the user to the register screen.
    """
    registerUser.registerUser()


# Class to create a user, setup here is the GUI
class create_account(tk.Frame):
    """
    This method sets up the tkinter window with the contents of the window(labels, buttons)
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create a Form label
        Label(self, text="Inspector - Grading Application", bg="grey", width="300", height="2",
              font=("Bold", 22)).pack()
        Label(self, text="").pack()

        Label(self, text="Register or Login below", width="300", height="2",
              font=("Bold", 20)).pack()

        # create Login Button
        Label(self, text="").pack()
        loginButton = Button(self, text="Login", command=login, width=10, height=1, font=("Calibri", 16), borderwidth=3)
        loginButton.pack()
        Label(self, text="").pack()
        # create a register button
        registerButton = Button(self, text="Register", command=register, width=10, height=1, font=("Calibri", 16),
                                borderwidth=3)
        registerButton.pack()


# Run files
if __name__ == "__main__":
    app = UserMainScreen()
    app.mainloop()
