import tkinter as tk

import UserInterface.programmedKeys
import UserInterface.GradingScheme
import UserInterface.FileAccess


class HomeScreen(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.geometry("800x800+100+100")
        self.title("Inspector - Grading Application")

        frame = MainFrame(container, self)
        self.frames[MainFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def changeProgButton():
    UserInterface.programmedKeys.programmedKeysWindow()


def saveProgButton():
    print("save programmed keys button pressed")


def changeGradingSchemeButton():
    print("change grading scheme button pressed")
    UserInterface.GradingScheme.gradingSchemeWindow()


def saveGradingSchemeButton():
    print("save grading scheme button pressed")


def proceedButton():
    print("Proceed Button pressed")
    UserInterface.FileAccess.fileDisplayWindow()


class MainFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl_title = tk.Label(self, text="Inspector - Grading Application", font=("Arial Bold", 20))
        lbl_title.place(x=400, y=50, anchor="center")

        about_text = tk.Label(self, width=58, height=40, relief="solid", bd=1, padx=10, bg="white")
        about_text.pack_propagate(0)
        tk.Label(about_text, bg="white", fg="black", text="About Inspector", font=("Calibri", 16)).pack()
        about_text.place(x=30, y=90)
        tk.Label(about_text, bg="white", fg="black",
                 text="\n\nInspector is a rapid-fire keystroke driven grading assessment\n"
                      + "application in which lecturers can grade assignments with a very\n "
                      + "high turnaround time and decrease the time spent of repetitive\n "
                      + " and rote tasks. The time taken to complete this tedious and  \n "
                      + " repetitive task can be significantly reduced by developing a \n"
                      + " keystroke driven application\n"
                      + "\n\nThe pre programmed keys and grading scheme can be tailored to\n"
                      + "suit your needs in order to assist you in the grading process", font=("Calibri", 12)).pack()
        about_text.place(x=30, y=90)

        # Created Label for pre programmed keys section
        prog_keys_lbl = tk.Label(self, width=40, height=19, relief="solid", bd=1, padx=10, bg="white")
        prog_keys_lbl.pack_propagate(0)

        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Pre-programmed Keys\n\n", font=("Calibri", 16)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key A =  2", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key B =  1", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key C = -1", font=("Calibri", 12)).pack()
        tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key D = -2", font=("Calibri", 12)).pack()
        prog_keys_lbl.place(x=470, y=90)

        # Create button for changing keys and saving changes
        prog_change_button = tk.Button(self, text="Change", fg="black", command=changeProgButton, height=1, width=6)
        prog_change_button.place(x=520, y=335)

        # Create button for changing keys and saving changes
        prog_save_button = tk.Button(self, text="Save", fg="black", command=saveProgButton, height=1, width=6)
        prog_save_button.place(x=700, y=335)

        # Created Label for grading scheme keys section
        grad_labl = tk.Label(self, width=40, height=20, relief="solid", bd=1, padx=10, bg="white")
        grad_labl.pack_propagate(0)

        # Create button for changing number of marks for assignment
        scheme_change_button = tk.Button(self, text="Change", fg="black", command=changeGradingSchemeButton, height=1,
                                         width=6)
        scheme_change_button.place(x=520, y=650)

        # Create button for changing keys and saving changes
        scheme_save_button = tk.Button(self, text="Save", fg="black", command=saveGradingSchemeButton, height=1,
                                       width=6)
        scheme_save_button.place(x=700, y=650)

        tk.Label(grad_labl, bg="white", fg="black", text="Grading Scheme\n", font=("Calibri", 15)).pack()
        tk.Label(grad_labl, bg="white", fg="black", text="Total marks out of 100", font=("Calibri", 12)).pack()
        tk.Label(grad_labl, bg="white", fg="black", text="\nUse the change button below to change\n total amount of "
                                                         "marks", font=("Calibri", 12)).pack()
        grad_labl.place(x=470, y=390)

        proceed_button = tk.Button(self, text="Proceed", fg="black", command=proceedButton, height=2, width=12)
        proceed_button.place(x=350, y=700)


app = HomeScreen()
app.mainloop()
