import os
import tkinter as tk
import UserInterface.DisplayAssignmentScreen
import UserInterface.InspectorMainScreen
import UserInterface.app
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *


class FileDisplayWindow(tk.Tk):

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
        self.resizable(False, False)

        frame = FileWindow(container, self)
        self.frames[FileWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(FileWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class FileWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Initializing error labels
        filepathErrorLbl = tk.Label(self, text="Please enter a filepath", font=("Arial", 8), fg="red")
        dirLabel = tk.Label(self, text="Directory Exists\t\t", font=("Arial", 8))
        errorLbl = tk.Label(self, text="Directory does not exists", font=("Arial", 8), fg="red")
        commentsEntry: Entry = tk.Entry(self, width="10")

        def clear():
            displayAssignment.config(state="active")
            # This clears the table when clear button is clicked
            listBox.delete(*listBox.get_children())
            filePath.delete('0', 'end')

        def printSelection():
            # Check if the filepath has been entered
            if filePath.get() != "":
                clicked_items = listBox.selection()
                print(listBox.item(clicked_items))
                # ToDo Get the entry file path from the entry box and concatenate it with the listbox selection
                # Get the filepath and add / in order to get the file
                st = filePath.get() + "/"
                # os.popen(st + listBox.item(clicked_items)['values'][0])
                selectAssignment()
                filepathErrorLbl.destroy()
            else:
                filepathErrorLbl.place(x=320, y=180)

        def back():
            # Have to fix this issue with closing the window using withdraw
            UserInterface.InspectorMainScreen.HomeScreen()

        def selectAssignment():
            print("Select Assignment button selected")
            UserInterface.DisplayAssignmentScreen.displayFileContents()

        def show():

            assignmentFilePath = filePath.get()

            if os.path.exists(assignmentFilePath):
                errorLbl.destroy()
                print("Directory Exists")
                dirLabel.place(x=320, y=180)

            else:
                print("Directory does not exists")
                errorLbl.place(x=320, y=180)
                dirLabel.destroy()

                # ToDo Have to add it so that it displays the files from the entered filepath in Entry box
                for filename in os.listdir(assignmentFilePath):
                    # ToDo Change filename for files in order to display all files in one line - Fix
                    tempList = [[filename]]

                    # Disable button after it has been clicked once in order for the data to only appear once
                    displayAssignment.config(state="disabled")
                    tempList.sort(key=lambda e: e[0], reverse=True)
                    # for i, (filename) in enumerate(tempList, start=1):

            # displays the folder and files in that folder
            abspath = os.path.abspath(assignmentFilePath)
            root_node = listBox.insert('', 'end', text=abspath, open=True)
            process_directory(root_node, abspath)

            return assignmentFilePath

            # This displays the files in a dir
            # for (file) in os.listdir(assignmentFilePath):
            #     listBox.insert("", "end", values=file)

        def process_directory(parent, assignmentFilePath):
            for file in os.listdir(assignmentFilePath):
                abspath = os.path.join(assignmentFilePath, file)
                isdir = os.path.isdir(abspath)
                print(isdir)
                oid = listBox.insert(parent, 'end', values=file, open=False)
                if isdir:
                    print("test")
                    process_directory(oid, abspath)

        def comments():
            # Entry for number of canned comments
            commentsLbl = tk.Label(self, fg="black", text="Enter number of comments: ", font=("Calibri", 12))
            commentsLbl.place(x=75, y=600)

            commentsEntry.place(x=265, y=605)
            commentsEntry.insert(0, "")

            enterButton = tk.Button(self, text="Enter", width=13, command=entryResult)
            enterButton.place(x=350, y=600)

        def entryResult():
            print("Enter button pressed")
            res = int(commentsEntry.get())
            window1 = tk.Tk()

            window1.title("Inspector - Grading Application")
            window1.geometry("400x400+200+200")
            window1.resizable(False, False)

            for col in range(res):
                commentsTitle = tk.Label(window1, fg="black", text="Comment " + str(col + 1), font=("Calibri", 12))
                commentsTitle.grid(row=col, column=5, padx=10, pady=10)
                commentsEntry1: Entry = tk.Entry(window1, width="30")
                commentsEntry1.grid(row=col, column=7, padx=10, pady=10)
                commentsEntry1.insert(0, "")
                saveButton = tk.Button(window1, text="Save", width=13, command=saveCommentsButton)
                saveButton.place(x=290, y=350)

        def saveCommentsButton():
            print("Save button pressed")

        # create Treeview with 3 columns
        cols = ('Filename', 'Graded', 'Grade')
        listBox = ttk.Treeview(self, columns=cols, show='headings')
        # set column headings
        for col in cols:
            listBox.heading(col, text=col)
            listBox.place(x=75, y=300)

        lbl_title = tk.Label(self, text="File Selection", font=("Arial Bold", 20))
        lbl_title.place(x=400, y=25, anchor="center")

        lbl_sub_title = tk.Label(self, text="List of Student Files", font=("Arial", 15))
        lbl_sub_title.place(x=400, y=250, anchor="center")

        lbl_student_files = tk.Label(self, text="Table of student files listed below",
                                     font=("Arial", 12))
        lbl_student_files.place(x=400, y=280, anchor="center")

        fileAccessPath = tk.Label(self, fg="black", text="FilePath - Students Assignments: ", font=("Calibri", 12))
        fileAccessPath.place(x=100, y=150)

        filePath: Entry = tk.Entry(self, width="35")
        filePath.place(x=320, y=155)
        filePath.insert(0, "")

        displayAssignment = tk.Button(self, text="Display Assignments", command=show, width=15)
        displayAssignment.place(x=550, y=150)

        clearButton = tk.Button(self, text="Clear", command=clear, height=1, width=6)
        clearButton.place(x=700, y=150)

        selectStudentAssignButton = tk.Button(self, text="Select Assignment", fg="black", command=printSelection,
                                              width=15)
        selectStudentAssignButton.place(x=280, y=550)

        backButton = tk.Button(self, text="Back", width=15, command=back)
        backButton.place(x=480, y=550)

        # ToDo add canned comments which will be incremental when one comment is added
        addComments = tk.Button(self, text="Add Canned Comment", width=18, command=comments)
        addComments.place(x=100, y=550)
