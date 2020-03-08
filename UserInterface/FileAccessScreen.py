import os
import queue
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from fpdf import FPDF

import UserInterface.InspectorMainScreen
import UserInterface.roughWork

# initialize queue for thread
the_queue = queue.Queue()


class FileDisplayWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.geometry("800x850+100+100")
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

        def changeKeyValues():
            global valueKeyA, valueKeyB, valueKeyC, valueKeyD
            global total

            # valueKeyA = int(input("Enter value for Key A: "))
            # valueKeyB = int(input("Enter value for Key B: "))
            # valueKeyC = int(input("Enter value for Key C: "))
            # valueKeyD = int(input("Enter value for Key D: "))
            # total = int(input("Enter total for grading: "))
            valueKeyA = 1
            valueKeyB = 1
            valueKeyC = 1
            valueKeyD = 1
            total = 2

        changeKeyValues()

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
            print(itemSelected)
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
            studentGrade = 0
            global fileExtension
            fileExtension = (".txt", ".py", "*", ".java", ".docx", ".c", ".cc", ".pdf")
            for studentFiles in os.listdir(assignmentFilePath):
                # Check if file ends with an extension, otherwise it is a folder
                if studentFiles.endswith(fileExtension):
                    abspath = os.path.join(assignmentFilePath, studentFiles)
                    isdir = os.path.isdir(abspath)
                    oid = listBox.insert(parentNode, 'end', values=("\t" + studentFiles, graded), open=False)
                    if isdir:
                        process_directory(oid, abspath)
                # Folder in the listbox
                else:
                    abspath = os.path.join(assignmentFilePath, studentFiles)
                    print(studentFiles)
                    oid2 = listBox.insert(parentNode, 'end', values=(studentFiles, " ", studentGrade), open=False)
                    process_directory(oid2, abspath)

        def canned_comments():

            comment1_lbl = tk.Label(self, fg="black", text="Comment 1: ", font=("Calibri", 12))
            comment1_lbl.place(x=75, y=554)
            commentsEntry1: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry1.place(x=170, y=552)
            comment2_lbl = tk.Label(self, fg="black", text="Comment 2: ", font=("Calibri", 12))
            comment2_lbl.place(x=75, y=594)
            commentsEntry2: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry2.place(x=170, y=592)
            comment3_lbl = tk.Label(self, fg="black", text="Comment 3: ", font=("Calibri", 12))
            comment3_lbl.place(x=75, y=634)
            commentsEntry3: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry3.place(x=170, y=632)
            comment4_lbl = tk.Label(self, fg="black", text="Comment 4: ", font=("Calibri", 12))
            comment4_lbl.place(x=75, y=674)
            commentsEntry4: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry4.place(x=170, y=672)
            comment5_lbl = tk.Label(self, fg="black", text="Comment 5: ", font=("Calibri", 12))
            comment5_lbl.place(x=75, y=714)
            commentsEntry5: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry5.place(x=170, y=712)

            def saveCommentsButton():

                global commentA, commentB, commentC, commentD, commentE
                print("Save button pressed")
                commentA = commentsEntry1.get("1.0", tk.END)
                print(commentA)
                commentB = commentsEntry2.get("1.0", tk.END)
                print(commentB)
                commentC = commentsEntry3.get("1.0", tk.END)
                print(commentC)
                commentD = commentsEntry4.get("1.0", tk.END)
                print(commentD)
                commentE = commentsEntry5.get("1.0", tk.END)
                print(commentE)

                # ToDo come up with a better solution to this
                commentsEntry1.destroy()
                commentsEntry2.destroy()
                commentsEntry3.destroy()
                commentsEntry4.destroy()
                commentsEntry5.destroy()
                comment1_lbl.destroy()
                comment2_lbl.destroy()
                comment3_lbl.destroy()
                comment4_lbl.destroy()
                comment5_lbl.destroy()
                saveButton.destroy()

            # Canned comments save button
            saveButton = tk.Button(self, text="Save", width=13, command=saveCommentsButton)
            saveButton.place(x=300, y=755)

        def back():
            # ToDo Have to fix this issue with closing the window using withdraw
            UserInterface.InspectorMainScreen.HomeScreen()

        # create Treeview with 3 list boxes
        cols = ('Student ID + files', 'Graded', 'Student Grade')
        listBox = ttk.Treeview(self, columns=cols, show='headings')

        # Added scrollbar onto the listbox
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=listBox.yview)
        listBox['yscroll'] = scrollbar.set

        scrollbar.place(in_=listBox, relx=1.0, relheight=1.0, bordermode="outside")
        # set column headings

        for col in cols:
            listBox.heading(col, text=col)
            listBox.place(x=75, y=270)

        lbl_title = tk.Label(self, text="Student File Selection", font=("Arial Bold", 20))
        lbl_title.place(x=400, y=35, anchor="center")

        fileAccessPath = tk.Label(self, fg="black", text="Enter File Path of Assignments: ", font=("Calibri", 12))
        fileAccessPath.place(x=75, y=150)

        filePath: tk.Entry = tk.Entry(self, width="35")
        filePath.place(x=300, y=155)
        filePath.insert(0, '')

        displayAssignment = tk.Button(self, text="Display Assignments", command=getFileSelection, width=15)
        displayAssignment.place(x=530, y=150)

        clearButton = tk.Button(self, text="Clear Path", command=clearEntry, height=1, width=13)
        clearButton.place(x=660, y=150)

        lbl_sub_title = tk.Label(self, text="List of Student Files", font=("Arial", 15))
        lbl_sub_title.place(x=400, y=220, anchor="center")

        lbl_student_files = tk.Label(self, text="Table of student files listed below", font=("Arial", 12))
        lbl_student_files.place(x=400, y=240, anchor="center")

        # Buttons at the bottom of the student file selection screen
        cannedCommentsButton = tk.Button(self, text="Canned Comments", width=15, command=canned_comments)
        cannedCommentsButton.place(x=320, y=510)

        selectStudentAssignButton = tk.Button(self, text="Select Assignment", fg="black", command=fileAccess, width=15)
        selectStudentAssignButton.place(x=550, y=510)

        backButton = tk.Button(self, text="Back", width=15, command=back)
        backButton.place(x=75, y=510)

        def selectAssignment():
            print("Select Assignment button selected")
            window = tk.Tk()
            window.title("Inspector - Grading Application")
            window.geometry("985x985+50+50")
            window.resizable(False, False)

            menubar = tk.Menu(window)

            global file
            global gradedFilesFolder
            fileExtension = (".txt", ".py", "*", ".java", ".docx", ".c", ".cc", ".pdf")

            # Get the click event of the selection from the listbox, use that selection to create a new filepath and add new graded files
            gradedFilesFolder = filePath.get().replace("\\", "/") + "/" + "/Graded Assignments" + "/" + selection + "/"
            print(gradedFilesFolder)
            if not os.path.exists(gradedFilesFolder):
                os.makedirs(gradedFilesFolder)

            # Check if listbox selection is a filename or a folder
            # If it is a filename, concat the string of the filepath and the filename
            if selection.endswith(fileExtension):
                file = filePath.get().replace("\\", "/") + "/" + str(item_text[0])

            # If it is a folder, concat the string of the filepath, the folder and the selection
            else:
                # Get the filename and remove the \t tab which is needed to display listbox with indentation
                file = filePath.get().replace("\\", "/") + "/" + selection + "/" + str(item_text[0])
                file = re.sub('\t', '', file)

            def back():
                # Clears listbox when returning to the file selection screen: this is in order to reselect the path
                # Call on_closingwindow() to save assignment if backbutton is pressed
                on_closingWindow()
                listBox.delete(*listBox.get_children())
                getFileSelection()

            def viewKeystrokes():
                print("View Keystrokes pressed")

            def howToVideo():
                print("Implement functionality to play video on window")

            # Menubar in the top left of the screen
            filemenu = tk.Menu(menubar, tearoff=0)
            # ToDo add the display with the keystrokes in this menu
            filemenu.add_command(label="View Keystrokes", command=viewKeystrokes)
            filemenu.add_separator()
            filemenu.add_command(label="Close Window", command=back)
            menubar.add_cascade(label="File", menu=filemenu)

            helpMenu = tk.Menu(menubar, tearoff=0)
            helpMenu.add_command(label="How to grade assignments?", command=howToVideo)
            menubar.add_cascade(label="Help", menu=helpMenu)

            # display the menu
            window.config(menu=menubar)

            # If window is closed mid grading, save the file in the folder
            def on_closingWindow():
                if messagebox.askokcancel("Quit", "Do you want to quit grading the assignment?\n File will be saved"):
                    s = text.get("1.0", tk.END)
                    f = open(file, "w", encoding='utf-8')
                    f.write(s)
                    f.close()
                    window.destroy()

            window.protocol("WM_DELETE_WINDOW", on_closingWindow)

            def submitAssignment():
                print("Submit button pressed")
                window.withdraw()
                # Opens file ans copies what is in tge text box and places back in file and saves
                s = text.get("1.0", tk.END)
                f = open(file, "w", encoding='utf-8')
                f.write(s)
                f.close()

                # Create a file for each student with their graded files
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 5, s)

                # Removed the \t from the filepath in order to save as pdf in 'Graded' file
                savingFilePDF = re.sub('\t', '', item_text[0] + ".pdf")
                print(savingFilePDF)
                pdf.output(gradedFilesFolder + "\\" + savingFilePDF)

            # Highlights code and text when text is selected and highlight button is pressed
            def highlightCode():
                global count
                count = 0
                count = 0
                if text.tag_ranges('sel'):
                    text.tag_add('color' + str(count), tk.SEL_FIRST, tk.SEL_LAST)
                    text.tag_configure('color' + str(count), foreground='red')
                    count += 1
                else:
                    # Do this if you want to overwrite all selection colors when you change color without selection
                    # for tag in text.tag_names():
                    #     text.tag_delete(tag)
                    text.config(foreground='yellow')

            # Keystroke driven application which is completed using threads and a thread queue as Tkinter is not thread safe
            # ToDo make if elif statement more efficient and faster
            def keystrokeApplication_thread():
                # ToDo enter keystroke in the entry box and use this as input fot the keystroke app
                keystroke = str(input())
                global total
                if keystroke.lower() == "s":

                    the_queue.put("Grading has started - Total marks: " + str(total))
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'a':

                    total += valueKeyA
                    the_queue.put("Key A: " + str(total) + " marks - " + "Implement comments for keys")
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'b':

                    total += valueKeyB
                    the_queue.put("Key B: " + str(total) + " marks - " + "Implement comments for keys")
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'c':

                    total -= valueKeyC
                    the_queue.put("Key C: " + str(total) + " marks - " + "Implement comments for keys")
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'd':

                    total -= valueKeyD
                    the_queue.put("Key D: " + str(total) + " marks - " + "Implement comments for keys")
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'e':

                    the_queue.put("Final Grade: " + str(total) + " marks")
                    keystrokeApplication_thread()

                elif keystroke == '1':
                    try:
                        commentA
                    except NameError:
                        the_queue.put("You have not added a comment for Key 1")
                        keystrokeApplication_thread()
                    else:
                        the_queue.put("Comment 1: " + commentA)
                        keystrokeApplication_thread()

                elif keystroke == '2':
                    try:
                        commentB
                    except NameError:
                        the_queue.put("You have not added a comment for Key 2")
                        keystrokeApplication_thread()
                    else:
                        the_queue.put("Comment 2: " + commentB)
                        keystrokeApplication_thread()

                elif keystroke == '3':
                    try:
                        commentC
                    except NameError:
                        the_queue.put("You have not added a comment for Key 3")
                        keystrokeApplication_thread()
                    else:
                        the_queue.put("Comment 3: " + commentC)
                        keystrokeApplication_thread()

                elif keystroke == '4':
                    try:
                        commentD
                    except NameError:
                        the_queue.put("You have not added a comment for Key 4")
                        keystrokeApplication_thread()
                    else:
                        the_queue.put("Comment 4: " + commentD)
                        keystrokeApplication_thread()

                elif keystroke == '5':
                    try:
                        commentE
                    except NameError:
                        the_queue.put("You have not added a comment for Key 5")
                        keystrokeApplication_thread()
                    else:
                        the_queue.put("Comment 5: " + commentE)
                        keystrokeApplication_thread()

                elif keystroke == 'z':
                    the_queue.empty()
                    keystrokeApplication_thread()

                else:
                    # let's tell queue_callback that this completed
                    print("Please enter a correct selection")
                    keystrokeApplication_thread()
                    print('keystrokeApplication_thread puts None to the queue')
                    the_queue.put(None)

            def queue_callback():
                try:
                    message = the_queue.get(block=False)

                except queue.Empty:
                    # retry
                    window.after(100, queue_callback)
                    return

                print("After_callback returned " + message)
                if message is not None:
                    # Print out the message once there is something in the queue
                    studentFinalGrade['text'] = message
                    # Insert messages from the queue into the text box
                    GradeTextBox.insert(tk.END, message + "\n")
                    # Scroll to the end of text when new text is added
                    GradeTextBox.see("end")
                    window.after(10, queue_callback)

            # Start the thread and run the keystrokeApplication_thread function
            threading.Thread(target=keystrokeApplication_thread).start()
            window.after(10, queue_callback)

            studentID = "Implement"

            assign_correction_lbl = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
            assign_correction_lbl.place(x=400, y=25, anchor="center")

            subTitle_lbl = tk.Label(window, text="Student: //" + studentID + "'s program", font=("Arial", 15))
            subTitle_lbl.place(x=400, y=70, anchor="center")

            shortcutLbl = tk.Label(window, text="Key Shortcuts", font=("Arial", 15))
            shortcutLbl.place(x=850, y=70, anchor="center")

            keysValue = tk.Label(window, text="   Key S: Start Grading" + "\n" + "Key A: +" + str(valueKeyA) + "\n"
                                                                                                               "Key B: +" + str(
                valueKeyB) + "\n"
                             "Key C: -" + str(
                valueKeyC) + "\n"
                             "Key D: -" + str(
                valueKeyD) + "\n"
                             "Key E: Exit grading", font=("Arial", 12))
            keysValue.place(x=850, y=150, anchor="center")

            studentFinalGrade = tk.Label(window, font=("Arial", 12))
            studentFinalGrade.place(x=800, y=245)

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
                           undo=True
                           )

            text.place(x=80, y=95)

            # Adding comments into the students grade textbox
            def addAssignmentComments():
                text.insert(tk.END, "\n\n***Grade/Comments***\n\n")
                text.insert(tk.INSERT, GradeTextBox.get("1.0", "end-1c"))

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

            GradeTextBox = tk.Text(window, wrap=tk.NONE, height=10, width=90, borderwidth=0)
            GradeTextBox.place(x=45, y=730)

            # Scrollbar on X and Y axis of GradeTextBox
            GradeTextBoxScrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=GradeTextBox.yview)
            GradeTextBox['yscroll'] = GradeTextBoxScrollbar.set

            GradeTextBoxScrollbar.place(in_=GradeTextBox, relx=1.0, relheight=1.0, bordermode="outside")

            addComments = tk.Button(window, text="Add comments above", width=25, command=addAssignmentComments)
            addComments.place(x=285, y=910)

            # Opens the file and copies the contents into the text box for editing
            global assignment
            assignment = open(file, encoding="ISO-8859-1").read()
            text.insert("1.0", assignment)


if __name__ == "__main__":
    app = FileDisplayWindow()
    app.mainloop()
    the_queue.put(None)
