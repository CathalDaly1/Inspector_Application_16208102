import tkinter as tk

import EmailSystem.emailSystem
import UsersAnalytics.userAnalytics
import GradingFunctionality.AccessingFiles
import UserCredentials.loginUser


def Homescreen():
    """This method creates the HomeScreen in the application. Creates contents of the tkinter window."""
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("800x800+100+100")

    # Get the time logged in from the loginUser file
    username = UserCredentials.loginUser.getUsername()
    lbl_title = tk.Label(window, text="Inspector - Grading Application", font=("Arial Bold", 20))
    lbl_title.place(x=400, y=70, anchor="center")

    username_lbl = tk.Label(window, fg="black", text="Welcome: " + str(username), font=("Calibri", 16))
    username_lbl.place(x=5, y=5)

    # Get the time logged in from the loginUser file
    time_logged_in = UserCredentials.loginUser.getTimeLoggedIn()
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
    prog_keys_lbl = tk.Label(window, width=100, height=21, relief="solid", bd=1, padx=10, bg="white")
    prog_keys_lbl.pack_propagate(0)

    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Pre-programmed Keys\n", font=("Calibri Bold", 16)).pack()
    tk.Label(prog_keys_lbl, bg="white", fg="black",
             text="In the next screen, enter the value of the pre-programmed keys and\n "
                  "comments in order to be able to select an assignment to grade. At the \n"
                  "bottom of this screen there are options to access the user analytics \n"
                  "and the Inspector Email system. \n", font=("Calibri", 12)).place(x=120, y=40)

    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Category A -> Ctrl + a", font=("Calibri", 12)).place(x=20,
                                                                                                               y=140)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Category B -> Ctrl + b", font=("Calibri", 12)).place(x=20,
                                                                                                               y=161)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Category C -> Ctrl + c", font=("Calibri", 12)).place(x=20,
                                                                                                               y=182)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Category D -> Ctrl + d", font=("Calibri", 12)).place(x=20,
                                                                                                               y=203)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Category E -> Ctrl + e", font=("Calibri", 12)).place(x=20,
                                                                                                               y=224)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Highlight text -> Ctrl + r", font=("Calibri", 12)).place(x=20,
                                                                                                             y=246)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key A -> +x marks", font=("Calibri", 12)).place(x=290, y=140)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key B -> +x marks", font=("Calibri", 12)).place(x=290, y=161)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key C -> +x marks", font=("Calibri", 12)).place(x=290, y=182)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key D -> +x marks", font=("Calibri", 12)).place(x=290, y=203)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key S -> Start Grading", font=("Calibri", 12)).place(x=290,
                                                                                                              y=224)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key E -> Complete Grading", font=("Calibri", 12)).place(x=290,
                                                                                                                 y=246)

    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 1 -> Canned Comment 1", font=("Calibri", 12)).place(x=520,
                                                                                                                 y=140)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 2 -> Canned Comment 2", font=("Calibri", 12)).place(x=520,
                                                                                                                 y=161)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 3 -> Canned Comment 3", font=("Calibri", 12)).place(x=520,
                                                                                                                 y=182)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 4 -> Canned Comment 4", font=("Calibri", 12)).place(x=520,
                                                                                                                 y=203)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Key 5 -> Canned Comment 5", font=("Calibri", 12)).place(x=520,
                                                                                                                 y=224)
    tk.Label(prog_keys_lbl, bg="white", fg="black", text="Submit Assignment -> Ctrl + s", font=("Calibri", 12)).place(x=520,
                                                                                                               y=246)
    prog_keys_lbl.place(x=30, y=400)

    quit_button = tk.Button(window, text="Quit Inspector", fg="red", command=quit, height=2, width=12,
                            font=("Calibri", 11))
    quit_button.place(x=30, y=730)

    view_analytics = tk.Button(window, text="View Analytics", fg="black",
                               command=UsersAnalytics.userAnalytics.analyticsScreen, height=2,
                               width=12, font=("Calibri", 11))
    view_analytics.place(x=250, y=730)

    send_emails = tk.Button(window, text="Email System", fg="black",
                            command=EmailSystem.emailSystem.emailSystem, font=("Calibri", 11), height=2, width=12)
    send_emails.place(x=450, y=730)

    proceed_button = tk.Button(window, text="Proceed", fg="black",
                               command=GradingFunctionality.AccessingFiles.FileDisplayWindow, height=2,
                               width=12, font=("Calibri", 11))
    proceed_button.place(x=650, y=730)
