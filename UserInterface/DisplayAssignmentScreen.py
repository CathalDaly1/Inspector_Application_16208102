import tkinter as tk
import UserInterface.FileAccessScreen
from UserInterface.FileAccessScreen import *


def displayFileContents():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("950x950+50+50")
    window.resizable(False, False)

    file = 'C:/Users/catha/OneDrive - University of Limerick/test2/10000001.txt'

    def back():
        window.withdraw()

    def submitAssignment():
        window.withdraw()
        print("Submit button pressed")

    # Highlights code when pressed
    # ToDo make it so it only highlights one selected code segment and not all of them in the code 
    def highlight():
        print("selected text: '%s'" % T.get(tk.SEL_FIRST, tk.SEL_LAST))

        s = T.get(tk.SEL_FIRST, tk.SEL_LAST)
        if s:
            # start from the beginning (and when we come to the end, stop)
            idx = '1.0'

            while 1:
                # find next occurrence, exit loop if no more
                idx = T.search(s, idx, nocase=1, stopindex=tk.END)
                if not idx: break
                # index right after the end of the occurrence

                lastidx = '%s+%dc' % (idx, len(s))
                # tag the whole occurrence (start included, stop excluded)
                T.tag_add('found', idx, lastidx)
                idx = lastidx
            T.tag_config('found', background='yellow')

    studentID = "Implement"

    lbl_title = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
    lbl_title.place(x=400, y=25, anchor="center")

    lbl_sub_title = tk.Label(window, text="Student: //" + studentID + "'s program", font=("Arial", 15))
    lbl_sub_title.place(x=400, y=70, anchor="center")

    # ToDo Get the name and student ID number of the student and display on this screen
    # ToDo Add keylogger in python in order to keep track of the totalling keys pressed in application
    # ToDo Display what keys have been pressed and there must be a way that the lecturer can remove choices if mistake has been made
    # ToDo Create a small table which will display logs and also display total amount of marks - LIVE

    # Created scroll bars horizontal and vertical in order to view code
    T = tk.Text(window, wrap=tk.NONE, height=35, width=90, borderwidth=0)
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=T.yview)
    T['yscroll'] = scrollbar.set

    scrollbarHor = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=T.xview)
    T['yscroll'] = scrollbar.set

    scrollbar.place(in_=T, relx=1.0, relheight=1.0, bordermode="outside")
    scrollbarHor.place(in_=T, rely=1.0, relwidth=1.0, bordermode="outside")
    T.place(x=45, y=90)

    backButton = tk.Button(window, text="Back", width=15, command=back)
    backButton.place(x=150, y=670)

    # ToDo once submit button has been pressed: decide where the lecturer is taken to next, probably back to assignment section
    submitButton = tk.Button(window, text="Submit", width=15, command=submitAssignment)
    submitButton.place(x=400, y=670)

    highlightButton = tk.Button(window, text="Highlight", width=15, command=highlight)
    highlightButton.place(x=550, y=670)

    T.insert(tk.END, open(file).read())
