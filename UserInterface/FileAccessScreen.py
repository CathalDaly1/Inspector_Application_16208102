import os
import threading
import tkinter as tk
from tkinter import ttk

from fpdf import FPDF

import UserInterface.DisplayAssignmentScreen
import UserInterface.InspectorMainScreen
import UserInterface.GradingSchemeScreen
import UserInterface.app
from multiprocessing import Process
from tkinter import *
from tkinter.colorchooser import *

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

        frame = FileSelectionWindow(container, self)
        self.frames[FileSelectionWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(FileSelectionWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class FileSelectionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Initializing error labels
        filepathErrorLbl = tk.Label(self, text="Please enter a filepath", font=("Arial", 8), fg="red")
        commentsEntry: tk.Entry = tk.Entry(self, width="10")
        global test

        def clearEntry():
            displayAssignment.config(state="active")
            # This clears the table when clear button is clicked
            listBox.delete(*listBox.get_children())
            filePath.delete('0', 'end')

        # Gets the file name of the selection of the listbox - achieved by 'text'
        def fileAccess():
            item = listBox.selection()[0]
            global itemSelected
            itemSelected = listBox.item(item, 'text')
            listboxSelection()

        # Gets the click of the element in the listbox in order to open file in the next window
        def doubleClickListboxEvent(event):
            item = listBox.selection()
            for i in item:
                global selection
                selection = listBox.item(i, "values")[0]
                print("You clicked: " + selection)

        def listboxSelection():
            # Check if the filepath has been entered
            if filePath.get() != "":
                global item_text
                global itemSelected
                # Get the item that has been selected and concats the string with the filepath and the filename selection
                # In order open the file; the full filepath and the name of the file must be selected
                for item in listBox.selection():
                    item_text = listBox.item(item, "values")
                    print((itemSelected + "/" + str(item_text)))

                selectAssignment()
                filepathErrorLbl.destroy()
            else:
                filepathErrorLbl.place(x=320, y=180)

        # Check of filepath has been entered and if it exists or not
        # If the directory exists then folders and files are displayed in the listbox
        # Displayed also is the status of the assignment grading = Y or N and the grade = 'Int'
        def getFileSelection():
            assignmentFilePath = filePath.get()

            # Check if the entered filepath exists on the users file system
            if os.path.exists(assignmentFilePath):
                print("Directory Exists")
                dirLabel = tk.Label(self, text="Directory Exists\t\t", font=("Arial", 8))
                dirLabel.place(x=320, y=180)

                # Loops through the files in the filepath and displays them
                for filename in os.listdir(assignmentFilePath):
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

                    # Double click on an element in the listbox will run the doubleClickListboxEvent() method
                    listBox.bind("<Double-Button-1>", doubleClickListboxEvent)

                    return assignmentFilePath

            else:
                print("Directory does not exists")
                errorLbl = tk.Label(self, text="Directory does not exists", font=("Arial", 8), fg="red")
                errorLbl.place(x=320, y=180)

        # Checks if file is in the directory, adds other columns if it is a file
        # ToDo maybe only add for folder as folder may contain many files which will be treated as one grade  Graded=N, Grade=0
        def process_directory(parentNode, assignmentFilePath):
            graded = "N"
            grade = 0
            global fileExtension
            fileExtension = (".txt", ".py", "*", ".java", ".docx", ".c", ".cc", ".pdf")
            for fileInDir in os.listdir(assignmentFilePath):
                # Check if file ends with an extension, otherwise it is a folder
                if fileInDir.endswith(fileExtension):
                    abspath = os.path.join(assignmentFilePath, fileInDir)
                    isdir = os.path.isdir(abspath)
                    oid = listBox.insert(parentNode, 'end', values=(fileInDir, graded, grade), open=False)
                    if isdir:
                        process_directory(oid, abspath)
                # Folder in the listbox
                else:
                    abspath = os.path.join(assignmentFilePath, fileInDir)
                    oid2 = listBox.insert(parentNode, 'end', values=fileInDir, open=False)
                    process_directory(oid2, abspath)

        def cannedComments():
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
                commentsEntry1: tk.Entry = tk.Entry(window1, width="30")
                commentsEntry1.grid(row=col, column=7, padx=10, pady=10)
                commentsEntry1.insert(0, "")
                saveButton = tk.Button(window1, text="Save", width=13, command=saveCommentsButton)
                saveButton.place(x=290, y=350)

        def saveCommentsButton():
            print("Save button pressed")

        def back():
            # Have to fix this issue with closing the window using withdraw
            UserInterface.InspectorMainScreen.HomeScreen()

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

        filePath: tk.Entry = tk.Entry(self, width="35")
        filePath.place(x=320, y=155)
        filePath.insert(0, '')

        displayAssignment = tk.Button(self, text="Display Assignments", command=getFileSelection, width=15)
        displayAssignment.place(x=550, y=150)

        clearButton = tk.Button(self, text="Clear", command=clearEntry, height=1, width=6)
        clearButton.place(x=700, y=150)

        selectStudentAssignButton = tk.Button(self, text="Select Assignment", fg="black", command=fileAccess,
                                              width=15)
        selectStudentAssignButton.place(x=280, y=550)

        backButton = tk.Button(self, text="Back", width=15, command=back)
        backButton.place(x=480, y=550)

        # ToDo add canned comments which will be incremental when one comment is added
        addComments = tk.Button(self, text="Add Canned Comment", width=18, command=cannedComments)
        addComments.place(x=100, y=550)

        def selectAssignment():
            print("Select Assignment button selected")
            window = tk.Tk()
            window.title("Inspector - Grading Application")
            window.geometry("950x950+50+50")
            window.resizable(False, False)

            global file
            global gradedFilesFolder
            fileExtension = (".txt", ".py", "*", ".java", ".docx", ".c", ".cc", ".pdf")

            gradedFilesFolder = filePath.get().replace("\\", "/") + "/Graded" + "/"
            if not os.path.exists(gradedFilesFolder):
                os.makedirs(gradedFilesFolder)

            # Check if listbox selection is a filename or a folder
            # If it is a filename, concat the string of the filepath and the filename
            if selection.endswith(fileExtension):
                file = filePath.get().replace("\\", "/") + "/" + str(item_text[0])

            # If it is a folder, concat the string of the filepath, the folder and the selection
            else:
                file = filePath.get().replace("\\", "/") + "/" + selection + "/" + str(item_text[0])

            def back():
                # Clears listbox when returning to the file selection screen: this is in order to reselect the path
                listBox.delete(*listBox.get_children())
                getFileSelection()
                window.withdraw()

            def submitAssignment():
                print("Submit button pressed")
                window.withdraw()
                # Opens file ans copies what is in tge text box and places back in file and saves
                s = text.get("1.0", tk.END)
                f = open(file, "w", encoding='utf-8')
                f.write(s)
                f.close()

                # ToDo Creates a PDF in from the text entered and saves as the name of the file
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 5, s)

                print(gradedFilesFolder)
                pdf.output(gradedFilesFolder + "\\" + item_text[0]+".pdf")

            # Highlights code and text when text is selected and highlight button is pressed
            def highlightCode():
                global count
                count = 0
                if text.tag_ranges('sel'):
                    text.tag_add('colortag_' + str(count), tk.SEL_FIRST, tk.SEL_LAST)
                    text.tag_configure('colortag_' + str(count), foreground='yellow')
                    count += 1
                else:
                    # Do this if you want to overwrite all selection colors when you change color without selection
                    # for tag in text.tag_names():
                    #     text.tag_delete(tag)
                    text.config(foreground='yellow')

            KeyA = 2
            KeyB = 1
            KeyC = -1
            KeyD = -2

            # Keystroke driven method in which the user can enter keys in order to store the students grade
            # ToDo find better solution of the threading in python and then write the keystroke driven method
            def keystrokeGrading():
                global total
                global total1
                keystroke = str(input())

                if keystroke.lower() == 's':
                    print("You have started the grading process")
                    total = 80
                    print(total)
                    keystrokeGrading()

                elif keystroke.lower() == 'a':
                    print("You pressed key a")
                    total += 2
                    print(total)
                    keystrokeGrading()

                elif keystroke.lower() == 'b':
                    print("You pressed key b")
                    total += 1
                    print(total)
                    keystrokeGrading()

                elif keystroke.lower() == "c":
                    print("You pressed key c")
                    total -= 1
                    print(total)
                    keystrokeGrading()

                elif keystroke.lower() == "d":
                    print("You pressed key d")
                    total -= 2
                    print(total)
                    keystrokeGrading()

                elif keystroke.lower() == 'e':
                    print("You pressed key e")
                    total1 = total
                    print("Total grade is: " + str(total1))

                else:
                    print("Incorrect Selection: Please choose (a,b,c,d)")
                    keystrokeGrading()

            threading.Thread(target=keystrokeGrading).start()

            studentID = "Implement"

            assign_correction_lbl = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
            assign_correction_lbl.place(x=400, y=25, anchor="center")

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

            lineNumbers = ''
            # The Text widget holding the line numbers.
            lnText = tk.Text(window,
                             width=2,
                             height=35,
                             padx=2,
                             highlightthickness=0,
                             takefocus=0,
                             bd=0,
                             background='lightgrey',
                             foreground='magenta',
                             state='disabled'
                             )
            lnText.place(x=55, y=95)

            # The Main Text Widget which contains the Assignment
            text = tk.Text(window,
                           width=85,
                           wrap=tk.NONE,
                           height=35,
                           bd=0,
                           padx=4,
                           undo=True,
                           background='white'
                           )

            text.place(x=80, y=95)

            # the_queue = queue.Queue()
            #
            # def keysTest_thread():
            #     on_click()
            #     # while True:
            #     #     message = the_queue.get()
            #     #     if message is None:
            #     #         print("thread_target: got None, exiting...")
            #     #         return
            #     #
            #     #     print("thread_target: doing something with", message, "...")
            #     #     time.sleep(1)
            #     #     print("thread_target: ready for another message")
            #
            # def on_click():
            #     keystroke = str(input())
            #     print(keystroke)
            #     a = 100
            #
            #     if keystroke.lower() == 's':
            #         print("You clicked: s")
            #         printOut = tk.Label(window, text="Final Grade: " + str(a) + "\n", font=("Arial", 12))
            #         printOut.place(x=850, y=250, anchor="center")
            #
            #     else:
            #         print("test")
            #
            # threading.Thread(target=keysTest_thread).start()

            # Scrollbar on X and Y axis of text box
            scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=text.yview)
            text['yscroll'] = scrollbar.set

            scrollbarHor = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=text.xview)
            text['yscroll'] = scrollbar.set

            scrollbar.place(in_=text, relx=1.0, relheight=1.0, bordermode="outside")
            scrollbarHor.place(in_=text, rely=1.0, relwidth=1.0, bordermode="outside")

            backButton2 = tk.Button(window, text="Back", width=15, command=back)
            backButton2.place(x=100, y=685)

            submitButton = tk.Button(window, text="Submit", width=15, command=submitAssignment)
            submitButton.place(x=300, y=685)

            highlightButton = tk.Button(window, text="Highlight", width=15, command=highlightCode)
            highlightButton.place(x=480, y=685)

            # Multiprocessing implemented
            p1 = Process(target=keystrokeGrading)
            beginGrading = tk.Button(window, text="Begin Grading", width=15, command=p1)
            beginGrading.place(x=680, y=685)

            GradeTextBox = tk.Text(window, wrap=tk.NONE, height=10, width=90, borderwidth=0)
            GradeTextBox.place(x=45, y=730)

            # Opens the file and copies the contents into the text box for editing
            global assignment
            assignment = open(file, encoding="ISO-8859-1").read()
            text.insert("1.0", assignment)
