import os
import threading
import tkinter as tk
from multiprocessing import Process

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

        def OnDoubleClick():
            item = listBox.selection()[0]
            print("you clicked on", listBox.item(item, "text"))
            global itemSelected
            itemSelected = listBox.item(item, 'text')
            printSelection()

        def printSelection():
            # Check if the filepath has been entered
            if filePath.get() != "":
                global item_text
                # clicked_items = listBox.selection()
                # # print(listBox.item(clicked_items))

                for item in listBox.selection():
                    item_text = listBox.item(item, "values")
                    print((itemSelected + "/" + str(item_text)))

                # ToDo Have to print the selection of the listboz
                # for item in listBox.selection():
                #     item_text = listBox.item(item, "text")
                #     print(item_text)
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
            window = tk.Tk()
            window.title("Inspector - Grading Application")
            window.geometry("950x950+50+50")
            window.resizable(False, False)

            global file
            file = filePath.get().replace("\\", "/") + "/" + str(item_text[0])
            print(file)
            # file = "C:/Users/catha/OneDrive - University of Limerick/test2/DocTest.txt"
            KeyA = 2
            KeyB = 1
            KeyC = -1
            KeyD = -2

            def back():
                window.withdraw()

            def submitAssignment():
                window.withdraw()
                # Opens file ans copys what was in T text box and places back in file and saves
                s = T.get("1.0", END)
                f = open(file, "w")
                f.write(s)
                f.close()
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

            def keys():
                global total
                global total1
                keystroke = str(input())

                if keystroke.lower() == 's':
                    print("You have started the grading process")
                    total = 80
                    print(total)
                    keys()

                elif keystroke.lower() == 'a':
                    print("You pressed key a")
                    total += 2
                    print(total)
                    keys()

                elif keystroke.lower() == 'b':
                    print("You pressed key b")
                    total += 1
                    print(total)
                    keys()

                elif keystroke.lower() == "c":
                    print("You pressed key c")
                    total -= 1
                    print(total)
                    keys()

                elif keystroke.lower() == "d":
                    print("You pressed key d")
                    total -= 2
                    print(total)
                    keys()

                elif keystroke.lower() == 'e':
                    print("You pressed key e")
                    total1 = total
                    print("Total grade is: " + str(total1))

                else:
                    print("Incorrect Selection: Please choose (a,b,c,d)")
                    keys()

            threading.Thread(target=keys).start()

            studentID = "Implement"

            lbl_title = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
            lbl_title.place(x=400, y=25, anchor="center")

            lbl_sub_title = tk.Label(window, text="Student: //" + studentID + "'s program", font=("Arial", 15))
            lbl_sub_title.place(x=400, y=70, anchor="center")

            shortcutLbl = tk.Label(window, text="Key Shortcuts", font=("Arial", 15))
            shortcutLbl.place(x=850, y=70, anchor="center")

            keysValue = tk.Label(window, text="Key A: +" + str(KeyA) + "\n"
                                                                       "Key B: +" + str(KeyB) + "\n"
                                                                                                "Key C: " + str(
                KeyC) + "\n"
                        "Key D: " + str(
                KeyD) + "\n"
                        "Key E: Exit grading", font=("Arial", 12))
            keysValue.place(x=850, y=150, anchor="center")

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

            # Multiprocessing implemented
            p1 = Process(target=keys)
            beginGrading = tk.Button(window, text="Begin Grading", width=15, command=p1)
            beginGrading.place(x=700, y=670)

            GradeTextBox = tk.Text(window, wrap=tk.NONE, height=10, width=90, borderwidth=0)
            GradeTextBox.place(x=45, y=715)

            global assignment
            assignment = open(file).read()
            T.insert("1.0", assignment)

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
            displayAssignment.config(state="disabled")
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

        selectStudentAssignButton = tk.Button(self, text="Select Assignment", fg="black", command=OnDoubleClick,
                                              width=15)
        selectStudentAssignButton.place(x=280, y=550)

        backButton = tk.Button(self, text="Back", width=15, command=back)
        backButton.place(x=480, y=550)

        # ToDo add canned comments which will be incremental when one comment is added
        addComments = tk.Button(self, text="Add Canned Comment", width=18, command=comments)
        addComments.place(x=100, y=550)
