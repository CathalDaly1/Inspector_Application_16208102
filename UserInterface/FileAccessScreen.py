import os
import queue
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2
from fpdf import FPDF
import UserInterface.loginUser

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
        self.geometry("800x900+100+100")
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
        self.controller = controller

        # Initializing error labels
        filepathErrorLbl = tk.Label(self, text="Please enter a filepath", font=("Arial", 8), fg="red")

        def connectToDB():
            connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
            try:
                return psycopg2.connect(connectionString)
            except:
                print("Cannot connect to the DB")

        conn = connectToDB()
        cur = conn.cursor()

        def clearEntry():
            displayAssignment.config(state="active")
            # This clears the table when clear button is clicked
            listBox.delete(*listBox.get_children())
            filePath.delete('0', 'end')

        # Gets the file name of the selection of the listbox - achieved by 'text'
        def fileAccess():
            try:
                item = listBox.selection()[0]
                global itemSelected
                itemSelected = listBox.item(item, 'text')
                listboxSelection()
                itemSelected_lbl = tk.Label(self, text='Item selected from list', font=("Arial", 9))
                itemSelected_lbl.place(x=400, y=259, anchor="center")

            except IndexError:
                itemSelectedError_lbl = tk.Label(self, text='Please select an item from the list below', fg="red",
                                                 font=("Arial", 9))
                itemSelectedError_lbl.place(x=400, y=259, anchor="center")

        # Gets the click of the element in the listbox in order to open file in the next window
        def doubleClickListboxEvent(event):
            item = listBox.selection()
            try:
                for i in item:
                    global selection
                    selection = listBox.item(i, "values")[0]
                    # ToDo fix this = fileSelection_errorlbl.destroy()
                    if selection.endswith('.txt'):
                        pass
                    else:
                        selection = listBox.item(i, "values")[0]
            except IndexError:
                pass

        def listboxSelection():
            # Check if the filepath has been entered
            if filePath.get() != "":
                global item_text
                # global itemSelected
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

            cur1 = conn.cursor()
            cur2 = conn.cursor()
            global fileExtension

            fileExtension = (".txt", ".py", "*", ".java", ".docx", ".c", ".cc", ".pdf")
            for studentFiles in os.listdir(assignmentFilePath):
                # Check if file ends with an extension, otherwise it is a folder
                abspath = os.path.join(assignmentFilePath, studentFiles)
                if studentFiles.endswith(fileExtension):
                    cur1.execute("SELECT graded_status FROM assignments WHERE filename =%s",
                                 (studentFiles,))
                    graded = cur1.fetchall()
                    cur2.execute("SELECT final_grade FROM assignments WHERE filename =%s",
                                 (studentFiles,))
                    studentGrade = cur2.fetchall()

                    isdir = os.path.isdir(abspath)
                    oid = listBox.insert(parentNode, 'end', values=(studentFiles, graded, studentGrade), open=False)
                    if isdir:
                        process_directory(oid, abspath)

                else:
                    cur1.execute("SELECT SUM(final_grade) FROM assignments WHERE student_id=%s",
                                 (studentFiles,))
                    studentGrade = cur1.fetchall()
                    oid3 = listBox.insert(parentNode, 'end', values=(studentFiles, " ", studentGrade), open=False)
                    process_directory(oid3, abspath)

        def changeKeyValues():

            keysHeading_lbl = tk.Label(self, fg="black", text="Enter Values for Keys and associated comments below",
                                       font=("Calibri Bold", 14))
            keysHeading_lbl.place(x=75, y=564)
            keyA_lbl = tk.Label(self, fg="black", text="Key A: ", font=("Calibri", 12))
            keyA_lbl.place(x=75, y=594)
            keyAEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyAEntry.place(x=170, y=592)
            keyAComment_lbl = tk.Label(self, fg="black", text="Comment A: ", font=("Calibri", 12))
            keyAComment_lbl.place(x=260, y=594)
            keyACommentEntry: tk.Text = tk.Text(self, height="2", width="35")
            keyACommentEntry.place(x=350, y=592)

            keyB_lbl = tk.Label(self, fg="black", text="Key B: ", font=("Calibri", 12))
            keyB_lbl.place(x=75, y=634)
            keyBEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyBEntry.place(x=170, y=632)
            keyBComment_lbl = tk.Label(self, fg="black", text="Comment B: ", font=("Calibri", 12))
            keyBComment_lbl.place(x=260, y=634)
            keyBCommentEntry: tk.Text = tk.Text(self, height="2", width="35")
            keyBCommentEntry.place(x=350, y=632)

            keyC_lbl = tk.Label(self, fg="black", text="Key C: ", font=("Calibri", 12))
            keyC_lbl.place(x=75, y=674)
            keyCEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyCEntry.place(x=170, y=672)
            keyCComment_lbl = tk.Label(self, fg="black", text="Comment C: ", font=("Calibri", 12))
            keyCComment_lbl.place(x=260, y=674)
            keyCCommentEntry: tk.Text = tk.Text(self, height="2", width="35")
            keyCCommentEntry.place(x=350, y=672)

            keyD_lbl = tk.Label(self, fg="black", text="Key D: ", font=("Calibri", 12))
            keyD_lbl.place(x=75, y=714)
            keyDEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyDEntry.place(x=170, y=712)
            keyDComment_lbl = tk.Label(self, fg="black", text="Comment D: ", font=("Calibri", 12))
            keyDComment_lbl.place(x=260, y=714)
            keyDCommentEntry: tk.Text = tk.Text(self, height="2", width="35")
            keyDCommentEntry.place(x=350, y=712)

            total_lbl = tk.Label(self, fg="black", text="Total Marks: ", font=("Calibri", 12))
            total_lbl.place(x=75, y=754)
            totalEntry: tk.Text = tk.Text(self, height="1", width="10")
            totalEntry.place(x=170, y=752)

            def saveKeysButton():
                global valueKeyA, valueKeyB, valueKeyC, valueKeyD, total, a, commentA, commentB, commentC, commentD, final
                try:
                    valueKeyA = int(keyAEntry.get("1.0", tk.END))
                    valueKeyB = int(keyBEntry.get("1.0", tk.END))
                    valueKeyC = int(keyCEntry.get("1.0", tk.END))
                    valueKeyD = int(keyDEntry.get("1.0", tk.END))
                    total = int(totalEntry.get("1.0", tk.END))
                    commentA = keyACommentEntry.get("1.0", tk.END)
                    commentB = keyBCommentEntry.get("1.0", tk.END)
                    commentC = keyCCommentEntry.get("1.0", tk.END)
                    commentD = keyDCommentEntry.get("1.0", tk.END)

                    a = int(total)
                    keysSaved_lbl = tk.Label(self, text="Values for Keys Saved", font=("Arial", 8))
                    keysSaved_lbl.place(x=320, y=570)

                    # Collapse key values entry's and labels when button is selected
                    keyAEntry.destroy()
                    keyBEntry.destroy()
                    keyCEntry.destroy()
                    keyDEntry.destroy()
                    totalEntry.destroy()
                    keyA_lbl.destroy()
                    keyB_lbl.destroy()
                    keyC_lbl.destroy()
                    keyD_lbl.destroy()
                    total_lbl.destroy()
                    keysHeading_lbl.destroy()
                    keyAComment_lbl.destroy()
                    keyACommentEntry.destroy()
                    keyBComment_lbl.destroy()
                    keyBCommentEntry.destroy()
                    keyCComment_lbl.destroy()
                    keyCCommentEntry.destroy()
                    keyDComment_lbl.destroy()
                    keyDCommentEntry.destroy()
                    saveButton.destroy()

                    changeKeyValuesButton = tk.Button(self, text="Change Keys values", width=15,
                                                      command=changeKeyValues)
                    changeKeyValuesButton.place(x=320, y=540)

                except ValueError:
                    keyValueError_lbl = tk.Label(self, text="Please enter values for all keys above", font=("Arial", 8),
                                                 fg="red")
                    keyValueError_lbl.place(x=270, y=775)

            saveButton = tk.Button(self, text="Save", width=13, command=saveKeysButton)
            saveButton.place(x=300, y=795)

        changeKeyValues()

        def canned_comments():

            comment1_lbl = tk.Label(self, fg="black", text="Comment 1: ", font=("Calibri", 12))
            comment1_lbl.place(x=75, y=594)
            commentsEntry1: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry1.place(x=170, y=592)
            comment2_lbl = tk.Label(self, fg="black", text="Comment 2: ", font=("Calibri", 12))
            comment2_lbl.place(x=75, y=634)
            commentsEntry2: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry2.place(x=170, y=632)
            comment3_lbl = tk.Label(self, fg="black", text="Comment 3: ", font=("Calibri", 12))
            comment3_lbl.place(x=75, y=674)
            commentsEntry3: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry3.place(x=170, y=672)
            comment4_lbl = tk.Label(self, fg="black", text="Comment 4: ", font=("Calibri", 12))
            comment4_lbl.place(x=75, y=714)
            commentsEntry4: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry4.place(x=170, y=712)
            comment5_lbl = tk.Label(self, fg="black", text="Comment 5: ", font=("Calibri", 12))
            comment5_lbl.place(x=75, y=754)
            commentsEntry5: tk.Text = tk.Text(self, height="2", width="63")
            commentsEntry5.place(x=170, y=752)

            def saveCommentsButton():
                global commentA, commentB, commentC, commentD, commentE
                print("Save button pressed")
                commentA = commentsEntry1.get("1.0", tk.END)
                commentB = commentsEntry2.get("1.0", tk.END)
                commentC = commentsEntry3.get("1.0", tk.END)
                commentD = commentsEntry4.get("1.0", tk.END)
                commentE = commentsEntry5.get("1.0", tk.END)
                # When save button is pressed, save the comments and destroy the entry's and labels
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
            saveButton.place(x=300, y=795)

        def back():
            # ToDo Have to fix this issue with closing the window using withdraw
            self.destroy()
            UserInterface.loginUser.Homescreen()

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
            window.geometry("1070x985+50+50")
            # window.resizable(False, False)

            menubar = tk.Menu(window)

            global file
            global gradedFilesFolder

            # Get the click event of the selection from the listbox, use that selection to create a new filepath and add new graded files
            gradedFilesFolder = filePath.get().replace("\\", "/") + "/" + "Graded Assignments" + "/" + selection + "/"
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
                # file = re.sub('\t', '', file)

            def viewKeystrokes():
                print("View Keystrokes pressed")

            def viewCannedComments():
                try:
                    commentsCombined = "Comment 1: " + commentA + "Comment 2: " + commentB + "Comment 3: " + commentC + "Comment 4: " + commentD + "Comment 5: " + commentE
                    messagebox.showinfo("Canned Comments", commentsCombined)

                except NameError:
                    messagebox.showinfo("Canned Comments", "You have not initialized all comments")

            def howToVideo():
                print("Implement functionality to play video on window")

            # Menubar in the top left of the screen
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="View Keystrokes", command=viewKeystrokes)
            file_menu.add_command(label="View Canned Comments", command=viewCannedComments)
            file_menu.add_separator()
            file_menu.add_command(label="Close Window", command=back)
            menubar.add_cascade(label="File", menu=file_menu)

            helpMenu = tk.Menu(menubar, tearoff=0)
            helpMenu.add_command(label="How to grade assignments?", command=howToVideo)
            menubar.add_cascade(label="Help", menu=helpMenu)

            # display the menu
            window.config(menu=menubar)

            # Keystroke driven application which is completed using threads and a thread queue as Tkinter is not thread safe
            # ToDo make if elif statement more efficient and faster
            def keystrokeApplication_thread():
                # ToDo enter keystroke in the entry box and use this as input for the keystroke app
                keystroke = str(input())
                global total
                global final
                if keystroke.lower() == "s":

                    print(total)
                    the_queue.put("Grading has started - Total marks: " + str(total))
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'a':

                    total += valueKeyA
                    the_queue.put("Key A: " + str(total) + " marks - " + commentA)
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'b':

                    total += valueKeyB
                    the_queue.put("Key B: " + str(total) + " marks - " + commentB)
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'c':

                    total -= valueKeyC
                    the_queue.put("Key C: " + str(total) + " marks - " + commentC)
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'd':

                    total -= valueKeyD
                    the_queue.put("Key D: " + str(total) + " marks - " + commentD)
                    keystrokeApplication_thread()

                elif keystroke.lower() == 'e':

                    the_queue.put("Final Grade: " + str(total) + " marks")
                    # sets the total to the initial value again
                    final = total

                    total = a
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
                    window.after(100, queue_callback)

            # Start the thread and run the keystrokeApplication_thread function
            thread = threading.Thread(target=keystrokeApplication_thread)
            thread.start()
            window.after(100, queue_callback)

            assign_correction_lbl = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
            assign_correction_lbl.place(x=400, y=25, anchor="center")

            subTitle_lbl = tk.Label(window, text="Student: " + selection + "'s Assignment", font=("Arial", 15))
            subTitle_lbl.place(x=400, y=70, anchor="center")

            keystrokes_lbl = tk.Label(window, width=30, height=22, relief="solid", bd=1, padx=10, bg="white")
            keystrokes_lbl.pack_propagate(0)
            keystrokes_lbl.place(x=790, y=95)
            tk.Label(keystrokes_lbl, bg="white", fg="black", text="Key Shortcuts", font=("Calibri Bold", 18)).pack()
            tk.Label(keystrokes_lbl, text="   Key S: Start Grading" + "\n" + "Key A: +" + str(valueKeyA) + "\n"
                                                                                                           "Key B: +" + str(
                valueKeyB) + "\n"
                             "Key C: -" + str(
                valueKeyC) + "\n"
                             "Key D: -" + str(
                valueKeyD) + "\n"
                             "Key E: Exit grading"
                                          + "\n"
                                            "Key 1: Comment 1"
                                          + "\n"
                                            "Key 2: Comment 2"
                                          + "\n"
                                            "Key 3: Comment 3"
                                          + "\n"
                                            "Key 4: Comment 4"
                                          + "\n"
                                            "Key 5: Comment 5",
                     font=("Arial", 12)).pack()

            studentFinalGrade = tk.Label(window, font=("Arial", 12))
            studentFinalGrade.place(x=790, y=430)

            GradeTextBox = tk.Text(window, wrap=tk.NONE, height=10, width=90, borderwidth=0)
            GradeTextBox.place(x=45, y=730)

            # Scrollbar on X and Y axis of GradeTextBox
            GradeTextBoxScrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=GradeTextBox.yview)
            GradeTextBox['yscroll'] = GradeTextBoxScrollbar.set
            GradeTextBox.insert(tk.END, "***Grade/Comments***\n")

            GradeTextBoxScrollbar.place(in_=GradeTextBox, relx=1.0, relheight=1.0, bordermode="outside")

            # Opens the file and copies the contents into the text box for editing
            global assignment
            assignment = open(file, encoding="ISO-8859-1").read()

            class TextLineNumbers(tk.Canvas):

                def __init__(self, *args, **kwargs):
                    tk.Canvas.__init__(self, *args, **kwargs)
                    self.textwidget = None

                def attach(self, text_widget):
                    self.textwidget = text_widget

                def redraw(self, *args):
                    '''redraw line numbers'''
                    self.delete("all")

                    i = self.textwidget.index("@0,0")
                    while True:
                        dline = self.textwidget.dlineinfo(i)
                        if dline is None: break
                        y = dline[1]
                        linenum = str(i).split(".")[0]
                        self.create_text(2, y, anchor="nw", text=linenum)
                        i = self.textwidget.index("%s+1line" % i)

            class CustomText(tk.Text):
                def __init__(self, *args, **kwargs):
                    tk.Text.__init__(self, *args, **kwargs)

                    # create a proxy for the underlying widget
                    self._orig = self._w + "_orig"
                    self.tk.call("rename", self._w, self._orig)
                    self.tk.createcommand(self._w, self._proxy)

                def _proxy(self, *args):
                    # let the actual widget perform the requested action
                    cmd = (self._orig,) + args
                    result = self.tk.call(cmd)

                    # generate an event if something was added or deleted,
                    # or the cursor position changed
                    if (args[0] in ("insert", "replace", "delete") or
                            args[0:3] == ("mark", "set", "insert")
                    ):
                        self.event_generate("<<Change>>", when="tail")

                    # return what the actual widget returned
                    return result

            class Example(tk.Frame):
                def __init__(self, *args, **kwargs):
                    tk.Frame.__init__(self, *args, **kwargs)
                    self.text = CustomText(self, width=84, wrap=tk.NONE, height=35)
                    self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
                    self.linenumbers = TextLineNumbers(self, width=30, bg="yellow")
                    self.linenumbers.attach(self.text)

                    self.linenumbers.pack(side="left", fill="y")
                    self.text.pack(side="right", fill="both", expand=True)

                    self.text.bind("<<Change>>", self._on_change)
                    self.text.bind("<Configure>", self._on_change)

                    scrollbarAssignment = tk.Scrollbar(window, orient=tk.VERTICAL, command=self.text.yview)
                    self.text['yscroll'] = scrollbarAssignment.set

                    scrollbarHor = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=self.text.xview)
                    self.text['xscroll'] = scrollbarHor.set

                    self.text.insert("end", assignment)

                    scrollbarAssignment.place(in_=self.text, relx=1.0, relheight=1.0, bordermode="outside")
                    scrollbarHor.place(in_=self.text, rely=1.0, relwidth=1.0, bordermode="outside")

                    addComments = tk.Button(window, text="Add comments above", width=25,
                                            command=self.addAssignmentComments)
                    addComments.place(x=285, y=910)

                    highlightButton = tk.Button(window, text="Highlight", width=15, command=self.highlightCode)
                    highlightButton.place(x=300, y=685)

                    submitButton = tk.Button(window, text="Submit", width=15, command=self.submitAssignment)
                    submitButton.place(x=480, y=685)

                    backButton2 = tk.Button(window, text="Back", width=15, command=self.back)
                    backButton2.place(x=100, y=685)

                def _on_change(self, event):
                    self.linenumbers.redraw()

                def submitAssignment(self):
                    print("Submit button pressed")
                    window.withdraw()
                    sql = "INSERT INTO assignments (student_id, filename, final_grade, graded_status) VALUES (%s, %s, %s, %s)"
                    val = (selection, item_text[0], final, 'Y')
                    # Executes the insertion ans passes values username and password into the insertion
                    cur.execute(sql, val)
                    conn.commit()
                    # Opens file ans copies what is in tge text box and places back in file and saves
                    s = self.text.get("1.0", tk.END)
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
                def highlightCode(self):
                    count = 0
                    if self.text.tag_ranges('sel'):
                        self.text.tag_add('color' + str(count), tk.SEL_FIRST, tk.SEL_LAST)
                        self.text.tag_configure('color' + str(count), foreground='red')
                        count += 1
                    else:
                        # Do this if you want to overwrite all selection colors when you change color without selection
                        # for tag in text.tag_names():
                        #     text.tag_delete(tag)
                        self.text.config(foreground='yellow')

                def addAssignmentComments(self):
                    self.text.insert(tk.END, "\n")
                    self.text.insert(tk.INSERT, GradeTextBox.get("1.0", "end-1c"))

                # If window is closed mid grading, save the file in the folder
                def on_closingWindow(self):
                    if messagebox.askokcancel("Quit",
                                              "Do you want to quit grading the assignment?\n File will be saved"):
                        self.submitAssignment()

                # ToDo implement window.protocol("WM_DELETE_WINDOW", on_closingWindow)

                def back(self):
                    # Clears listbox when returning to the file selection screen: this is in order to reselect the path
                    # Call on_closingwindow() to save assignment if backbutton is pressed
                    self.on_closingWindow()
                    listBox.delete(*listBox.get_children())
                    getFileSelection()

            Example(window).place(x=60, y=95)


if __name__ == "__main__":
    app = FileDisplayWindow()
    app.mainloop()
    the_queue.put(None)
