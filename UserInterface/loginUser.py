import datetime
import hashlib
import tkinter as tk
import psycopg2
import UserInterface.FileAccessScreen
from tkinter import *
import UserInterface.registerUser


class LoginUserScreen(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Creates the GUI window, sets size of the window
        self.frames = {}
        self.geometry("300x250+400+300")
        self.title("Inspector - Grading Application")
        # Window can not be increased or decreased in size
        self.resizable(False, False)

        # Links the Homescreen GUI with the MainFrame class
        frame = LoginFrame(container, self)
        self.frames[LoginFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginFrame)

    # Displays the window
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def proceedButton():
    print("Proceed Button pressed")
    UserInterface.FileAccessScreen.FileDisplayWindow()


def Homescreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("800x800+100+100")

    lbl_title = tk.Label(window, text="Inspector - Grading Application", font=("Arial Bold", 20))
    lbl_title.place(x=400, y=50, anchor="center")

    username_lbl = tk.Label(window, fg="black", text="Welcome: " + username1, font=("Calibri", 16))
    username_lbl.place(x=5, y=5)

    loggedIn_lbl = tk.Label(window, fg="black", text="Logged in: " + str(time_logged_in), font=("Calibri", 12))
    loggedIn_lbl.place(x=535, y=5)

    about_text = tk.Label(window, width=100, height=19, relief="solid", bd=1, padx=10, bg="white")
    about_text.pack_propagate(0)
    tk.Label(about_text, bg="white", fg="black", text="About Inspector", font=("Calibri Bold", 18)).pack()
    about_text.place(x=30, y=100)
    tk.Label(about_text, bg="white", fg="black",
             text="\nInspector is a rapid-fire keystroke driven grading assessment\n"
                  + "application in which lecturers can grade assignments with a\n "
                  + "high turnaround time and decrease the time spent of repetitive\n "
                  + " and rote tasks. The time taken to complete this tedious and  \n "
                  + " repetitive task can be significantly reduced by developing a \n"
                  + " keystroke driven application.\n"
                  + "\n\nThe pre programmed keys and grading scheme can be tailored\n"
                  + "to suit your needs in order to assist you in the grading process.\n",
             font=("Calibri", 12)).pack()

    # Created Label for pre programmed keys section
    prog_keys_lbl = tk.Label(window, width=100, height=19, relief="solid", bd=1, padx=10, bg="white")
    prog_keys_lbl.pack_propagate(0)

    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Pre-programmed Keys\n", font=("Calibri Bold", 16)).pack()
    tk.Label(prog_keys_lbl, bg="white", fg="black",
             text="Key values can be changed after the\n proceed button is selected", font=("Calibri", 12)).pack()
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key A = +x marks", font=("Calibri", 12)).place(x=200, y=120)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key B = +x marks", font=("Calibri", 12)).place(x=200, y=140)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key C = -x marks", font=("Calibri", 12)).place(x=200, y=160)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key D = -x marks", font=("Calibri", 12)).place(x=200, y=180)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key S = Start Grading", font=("Calibri", 12)).place(x=200,
                                                                                                              y=200)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key E = End Grading", font=("Calibri", 12)).place(x=200,
                                                                                                            y=222)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 1 = Comment 1", font=("Calibri", 12)).place(x=400, y=120)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 2 = Comment 2", font=("Calibri", 12)).place(x=400, y=140)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 3 = Comment 3", font=("Calibri", 12)).place(x=400, y=160)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 4 = Comment 4", font=("Calibri", 12)).place(x=400, y=180)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 5 = Comment 5", font=("Calibri", 12)).place(x=400, y=200)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key Q = Quit Inspector", font=("Calibri", 12)).place(x=400,
                                                                                                               y=222)

    prog_keys_lbl.place(x=30, y=400)

    quit_button = tk.Button(window, text="Quit Inspector", fg="red", command=quit, height=2, width=12)
    quit_button.place(x=250, y=700)

    proceed_button = tk.Button(window, text="Proceed", fg="black", command=proceedButton, height=2, width=12)
    proceed_button.place(x=500, y=700)


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        username_verify = StringVar()
        password_verify = StringVar()

        global username_login_entry
        global password_login_entry

        # Connects to the database
        # ToDo Place this into one file and instantiate into the REST API
        def connectToDB():
            connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
            try:
                return psycopg2.connect(connectionString)
            except:
                print("Cannot connect to the DB")

        conn = connectToDB()
        cur = conn.cursor()
        cur1 = conn.cursor()

        def back():
            LoginFrame.destroy(self)

        # Checks if the username and password are in the database
        def login_verify():
            global username1
            global time_logged_in
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

            cur.execute("SELECT account_created  FROM Users WHERE username =%s and password =%s",
                        (username1, t_password,))
            time_created = cur.fetchall()
            print("Account created on: ", time_created)
            time_logged_in = datetime.datetime.now()

            # Check if there is data in the database
            # Loops through the username's and passwords
            # Creates a set of [Username, password] and checks if they match
            errorLbl = tk.Label(self, text="Incorrect Username or password", font=("Arial", 8), fg="red")
            if rows:
                for row in rows:
                    if username1 == row[0] or password1 == row[1]:
                        Homescreen()
                        # LoginFrame.destroy(self)
            else:
                # Clears the text in the entry box
                username_entry.delete('0', 'end')
                password_entry.delete('0', 'end')
                errorLbl.place(x=60, y=125)

        Label(self, text="Please enter your details below").pack()
        Label(self, text="").pack()
        Label(self, text="Username").pack()
        username_entry = Entry(self, textvariable=username_verify)
        username_entry.pack()
        Label(self, text="Password").pack()
        password_entry = Entry(self, show="*", textvariable=password_verify)
        password_entry.pack()
        Label(self, text="\n").pack()
        Button(self, text="Login", width=10, height=1, command=login_verify).pack()
        Button(self, text="Back", width=10, height=1, command=back).pack()
