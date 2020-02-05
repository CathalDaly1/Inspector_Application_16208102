import os
import tkinter as tk
import UserInterface.DisplayAssignmentScreen
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *


def fileDisplayWindow():
    window = tk.Tk()

    window.title("Inspector - Grading Application")
    window.geometry("800x800+100+100")
    window.resizable(False, False)

    def clear():
        displayAssignment.config(state="active")
        # This clears the table when clear button is clicked
        listBox.delete(*listBox.get_children())
        filePath.delete('0', 'end')

    def printSelection():
        clicked_items = listBox.selection()
        print(listBox.item(clicked_items))
        # ToDo Get the entry file path from the entry box and concatenate it with the listbox selection
        st = 'C:/Users/catha/OneDrive - University of Limerick/test2/'
        os.popen(st + listBox.item(clicked_items)['values'][0])
        selectAssignment()

    def back():
        window.withdraw()

    def selectAssignment():

        print("Select Assignment button selected")
        UserInterface.DisplayAssignmentScreen.displayFileContents()
        window.withdraw()

    def show():

        assignmentFilePath = filePath.get()
        dirLabel = tk.Label(window, text="Directory Exists\t\t", font=("Arial", 8))
        errorLbl = tk.Label(window, text="Directory does not exists", font=("Arial", 8), fg="red")

        if os.path.exists(assignmentFilePath):
            errorLbl.destroy()
            print("Directory Exists")
            dirLabel.place(x=320, y=180)

        else:
            print("Directory does not exists")
            errorLbl.place(x=320, y=180)
            dirLabel.destroy()

        with open("files.txt", "w") as a:
            for path, subdirs, files in os.walk(assignmentFilePath):
                for filename in files:
                    a.write(str(filename + "\n"))

                # ToDo Have to add it so that it displays the files from the entered filepath in Entry box
                for filename in os.listdir(assignmentFilePath):
                    # ToDo Change filename for files in order to display all files in one line - Fix
                    tempList = [[filename]]

                # Disable button after it has been clicked once in order for the data to only appear once
                displayAssignment.config(state="disabled")
                tempList.sort(key=lambda e: e[0], reverse=True)
                # for i, (filename) in enumerate(tempList, start=1):

                for (file) in os.listdir(assignmentFilePath):
                    listBox.insert("", "end", values=file)

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

    selectStudentAssignButton = tk.Button(window, text="Select Assignment", fg="black", command=printSelection,
                                          width=15)
    selectStudentAssignButton.place(x=250, y=550)

    backButton = tk.Button(window, text="Back", width=15, command=back)
    backButton.place(x=450, y=550)
