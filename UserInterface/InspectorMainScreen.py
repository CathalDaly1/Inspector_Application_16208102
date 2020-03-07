import tkinter as tk

from PIL import ImageTk, Image

import UserInterface.ProgrammedKeysScreen
import UserInterface.FileAccessScreen
import UserInterface.loginUser
from UserInterface.loginUser import *


# Initialisation of the Homescreen of Inspector
class HomeScreen(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Creates the GUI window, sets size of the window
        self.frames = {}
        self.geometry("800x800+100+100")
        self.title("Inspector - Grading Application")
        # Window can not be increased or decreased in size
        self.resizable(False, False)

        # Links the Homescreen GUI with the MainFrame class
        frame = MainFrame(container, self)
        self.frames[MainFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainFrame)

    # Displays the window
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def proceedButton():
    print("Proceed Button pressed")
    UserInterface.FileAccessScreen.FileDisplayWindow()


# MainFrame contains the contents of the GUI
class MainFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # ToDo add image to the top of the screen

        lbl_title = tk.Label(self, text="Inspector - Grading Application", font=("Arial Bold", 20))
        lbl_title.place(x=400, y=50, anchor="center")

        about_text = tk.Label(self, width=58, height=19, relief="solid", bd=1, padx=10, bg="white")
        about_text.pack_propagate(0)
        tk.Label(about_text, bg="white", fg="black", text="About Inspector", font=("Calibri Bold", 16)).pack()
        about_text.place(x=30, y=300)
        tk.Label(about_text, bg="white", fg="black",
                 text="\n\nInspector is a rapid-fire keystroke driven grading assessment\n"
                      + "application in which lecturers can grade assignments with a\n "
                      + "high turnaround time and decrease the time spent of repetitive\n "
                      + " and rote tasks. The time taken to complete this tedious and  \n "
                      + " repetitive task can be significantly reduced by developing a \n"
                      + " keystroke driven application.\n"
                      + "\n\nThe pre programmed keys and grading scheme can be tailored\n"
                      + "to suit your needs in order to assist you in the grading process.\n",
                 font=("Calibri", 12)).pack()

        # Created Label for pre programmed keys section
        prog_keys_lbl = tk.Label(self, width=40, height=19, relief="solid", bd=1, padx=10, bg="white")
        prog_keys_lbl.pack_propagate(0)

        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Pre-programmed Keys\n", font=("Calibri Bold", 16)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black",
                 text="Click the change button below to change\n keystroke values\n", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key A = +2", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key B = +1", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key C = -1", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key D = -2", font=("Calibri", 12)).pack()
        prog_keys_lbl.place(x=470, y=300)

        quit_button = tk.Button(self, text="Quit Inspector", fg="red", command=self.quit, height=2, width=12)
        quit_button.place(x=300, y=700)

        proceed_button = tk.Button(self, text="Proceed", fg="black", command=proceedButton, height=2, width=12)
        proceed_button.place(x=400, y=700)


if __name__ == "__main__":
    app = HomeScreen()
    app.mainloop()
