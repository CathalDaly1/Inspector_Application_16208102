import os
import tkinter as tk
import UserInterface.DisplayStudentProgram
from tkinter import filedialog, ttk, Entry
from tkinter.ttk import *


def fileDisplayWindow():
    window = tk.Tk()

    window.title("Inspector - Grading Application")
    window.geometry("800x800+100+100")

    def clear():
        displayAssignment.config(state="active")
        # ToDo Implement clearing the listbox when clear is added in order to reset the table = Status red

        filePath.delete('0', 'end')

    def back():
        window.withdraw()

    def selectAssignment():
        print("Select Assignment button selected")
        UserInterface.DisplayStudentProgram.displayFileContents()

    def show():

        test1 = filePath.get()
        path1 = os.path.realpath(test1)

        # Have to fix this in order to destroy the label after new label appears
        dirLabel = tk.Label(window, text="Directory Exists\t\t", font=("Arial", 8))
        errorLbl = tk.Label(window, text="Directory does not exists", font=("Arial", 8), fg="red")

        if os.path.exists(test1):
            os.startfile(path1)
            errorLbl.destroy()
            print("Directory Exists")
            dirLabel.place(x=320, y=180)

        else:
            print("Directory does not exists")
            errorLbl.place(x=320, y=180)
            dirLabel.destroy()

        with open("files.txt", "w") as a:
            for path, subdirs, files in os.walk(test1):
                for filename in files:
                    a.write(str(filename + "\n"))

                # ToDo Have to add it so that it displays the files from the entered filepath in Entry box
                for filename in os.listdir(test1):
                    # ToDo Change filename for files in order to display all files in one line - Fix
                    tempList = [[filename]]

                # Disable button after it has been clicked once in order for the data to only appear once
                displayAssignment.config(state="disabled")
                tempList.sort(key=lambda e: e[0], reverse=True)
                # for i, (filename) in enumerate(tempList, start=1):
                for (file) in os.listdir(test1):
                    listBox.insert("", "end", values=file)
                    #print(os.path.splitext("StudentID: " + filename)[0])


    # create Treeview with 3 columns
    cols = ('Filename', 'Graded', 'Grade')
    listBox = ttk.Treeview(window, columns=cols, show='headings')
    # set column headings
    for col in cols:
        listBox.heading(col, text=col)
        listBox.place(x=75, y=300)

    lbl_title = tk.Label(window, text="File Selection", font=("Arial Bold", 20))
    lbl_title.place(x=400, y=25, anchor="center")

    lbl_sub_title = tk.Label(window, text="List of Student Files", font=("Arial", 15))
    lbl_sub_title.place(x=400, y=250, anchor="center")

    lbl_student_files = tk.Label(window, text="Table of student files listed below //Implement this functionality",
                                 font=("Arial", 12))
    lbl_student_files.place(x=400, y=280, anchor="center")

    fileAccessPath = tk.Label(window, fg="black", text="FilePath - Students Assignments: ", font=("Calibri", 12))
    fileAccessPath.place(x=100, y=150)

    filePath: Entry = tk.Entry(window, width="35")
    filePath.place(x=320, y=155)
    filePath.insert(0, "")

    displayAssignment = tk.Button(window, text="Display Assignments", command=show, width=15)
    displayAssignment.place(x=550, y=150)

    clearButton = tk.Button(window, text="Clear", command=clear, height=1, width=6)
    clearButton.place(x=700, y=150)

    selectStudentAssignButton = tk.Button(window, text="Select Assignment", fg="black", command=selectAssignment,
                                          width=15)
    selectStudentAssignButton.place(x=250, y=550)

    closeButton = tk.Button(window, text="Close", width=15, command=exit)
    closeButton.place(x=450, y=550)

    proceed_button = tk.Button(window, text="Back", fg="black", command=back, height=2, width=12)
    proceed_button.place(x=350, y=700)
