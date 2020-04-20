import os
import queue
import re
import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2
from PIL import ImageTk

import DBConnection.connectToDB
import GradingFunctionality.cannedComments
import UserCredentials.loginUser
import UserCredentials.LoginRegistrationScreen
import GradingFunctionality.ChangingGrades
import GradingFunctionality.AssignmentGrading

# initialize queue for thread
the_queue = queue.Queue()


class FileDisplayWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,
                         default='C:/Users/catha/PycharmProjects/Inspector_Application/InspectorImage/Inspector.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
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
        self.controller = controller

        # Initializing error labels
        filepathErrorLbl = tk.Label(self, text="Please enter a filepath", font=("Arial", 8), fg="red")

        conn = DBConnection.connectToDB.connectToDB()
        cur = conn.cursor()

        def saveModuleCode():
            global assignmentModuleCode, assignmentNo
            assignmentModuleCode = enterModuleCode.get().upper()
            assignmentNo = enterAssignmentNo.get().upper()
            if assignmentNo and assignmentModuleCode != "":
                moduleCodeSaved_lbl = tk.Label(self, text="Module code and Assignment No. saved\t\t")
                moduleCodeSaved_lbl.place(x=527, y=87)
            else:
                moduleCodeSaved_lbl = tk.Label(self, text="Module code and Assignment No. Not saved\t\t", fg="red")
                moduleCodeSaved_lbl.place(x=527, y=87)

        def clearEntry():
            displayAssignment.config(state="active")
            # This clears the table when clear button is clicked
            listBox.delete(*listBox.get_children())
            filePath.delete('0', 'end')
            enterModuleCode.delete('0', 'end')
            enterAssignmentNo.delete('0', 'end')

        # Gets the file name of the selection of the listbox - achieved by 'text'
        def fileAccess():
            global assignmentModuleCode, assignmentNo
            assignmentModuleCode = enterModuleCode.get()
            assignmentNo = enterAssignmentNo.get()
            try:
                if assignmentModuleCode and assignmentNo != "":
                    saveModuleCode()
                else:
                    moduleCodeError_lbl = tk.Label(self, text="Please enter Module Code and Assignment No.", fg="red")
                    moduleCodeError_lbl.place(x=527, y=85)
                    displayAssignment.config(state="active")

                item = listBox.selection()[0]
                global itemSelected
                itemSelected = listBox.item(item, 'text')
                listboxSelection()

            except IndexError:
                itemSelectedError_lbl = tk.Label(self, text='Please select an item from the list below', fg="red",
                                                 font=("Arial", 9))
                itemSelectedError_lbl.place(x=380, y=460, anchor="center")

        def refreshListbox():
            listBox.delete(*listBox.get_children())
            assignmentPath = filePath.get()
            abspath = os.path.abspath(assignmentPath)
            root_node = listBox.insert('', 'end', text=abspath, open=True)
            process_directory(root_node, abspath)

        def onClickEvent(event):
            try:
                if assignmentNo and assignmentModuleCode != "":
                    refreshListbox()
            except NameError as error:
                print(error)

        # Bind the click event to mouse click(Left click)
        self.bind("<1>", onClickEvent)

        # Gets the click of the element in the listbox in order to open file in the next window
        def doubleClickListboxEvent(event):
            item = listBox.selection()
            try:
                for i in item:
                    global selection
                    selection = listBox.item(i, "values")[0]
                    treeviewFileExtension = re.search(r'\.\w+$', selection)
                    # ToDo fix this = fileSelection_errorlbl.destroy()
                    if treeviewFileExtension is not None:
                        pass
                    else:
                        selection = listBox.item(i, "values")[0]
            except IndexError as error:
                print("Cannot select " + str(error))

        def selectAssignment():
            GradingFunctionality.AssignmentGrading.selectAssignment()

        def infoLabel():
            global infoText_lbl
            infoText_lbl = tk.Label(self, text="Open Assignment: Double Click Student ID.\n"
                                               "Click once on filename, click 'Select Assignment'",  anchor='w', fg="red", font=("Arial", 10))
            infoText_lbl.place(x=510, y=173)
            deleteInfoLabel()

        def deleteInfoLabel():
            self.after(10000, infoText_lbl.destroy)
            refreshListbox()

        def listboxSelection():
            # Check if the filepath has been entered
            if filePath.get() != "":
                global item_text
                # global itemSelected
                # Get the item that has been selected and concats the string with the filepath and the filename selection
                # In order open the file; the full filepath and the name of the file must be selected
                for item in listBox.selection():
                    item_text = listBox.item(item, "values")
                userID = UserCredentials.loginUser.getUserID()

                try:
                    cur.execute(
                        "SELECT * FROM assignments WHERE user_id =%s and student_id = %s and filename = %s and modulecode=%s and assignmentNo=%s",
                        (userID, selection, item_text[0], assignmentModuleCode, assignmentNo))
                    vals = cur.fetchone()
                    conn.commit()

                    if vals is not None:
                        if str(vals[1]) == str(userID) and str(vals[4]) == str(selection) and str(vals[5]) == str(
                                item_text[0]):
                            result = messagebox.askquestion("Inspector Grading",
                                                            "Do you want to regrade this assignment?")

                            if result == 'yes':
                                selectAssignment()
                                filepathErrorLbl.destroy()
                            else:
                                print("Close message box")
                    else:
                        selectAssignment()
                        filepathErrorLbl.destroy()

                except (psycopg2.Error, AttributeError):
                    refreshListbox()
                    infoLabel()

            else:
                filepathErrorLbl.place(x=320, y=180)

        '''Check of filepath has been entered and if it exists or not
        if the directory exists then folders and files are displayed in the listbox
        Displayed also is the status of the assignment grading = Y or N and the grade = 'Int'''

        def getFileSelection():
            saveModuleCode()
            global assignmentFilePath
            assignmentFilePath = filePath.get()

            # Check if the entered filepath exists on the users file system
            if os.path.exists(assignmentFilePath) and assignmentModuleCode and assignmentNo != "":
                dirLabel = tk.Label(self, text="Directory Exists\t\t", font=("Calibri", 9))
                dirLabel.place(x=340, y=142)

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

                    # ToDo Look into cleaning this up. Not fully working yet. Need text boxes to disappear when new module is searched and is already in the db
                    userID = UserCredentials.loginUser.getUserID()
                    if moduleCode and assignmentNo != "":
                        cur.execute(
                            "SELECT * FROM keyscomments WHERE user_id =%s and modulecode = %s and assignmentno = %s",
                            (userID, assignmentModuleCode, assignmentNo))
                        vals = cur.fetchone()

                        if vals is None:
                            changeKeyValues()
                        else:
                            changeKeyValuesButton = tk.Button(self, text="Change Keys values", width=15,
                                                              command=changeKeyValues)
                            changeKeyValuesButton.place(x=320, y=500)
                    else:
                        moduleCodeSaved_lbl = tk.Label(self, text="Please enter the Module Code and Assignment No.\t\t",
                                                       fg="red")
                        moduleCodeSaved_lbl.place(x=527, y=85)

                    # Double click on an element in the listbox will run the doubleClickListboxEvent() method
                    # refreshListbox()
                    listBox.bind("<Double-Button-1>", doubleClickListboxEvent)
                refreshListbox()
            else:
                directoryErrorLbl = tk.Label(self, text="Directory does not exists", font=("Calibri", 9), fg="red")
                directoryErrorLbl.place(x=340, y=142)

        '''Checks if file is in the directory, adds other columns if it is a file
        display data from the database into the to treeview
        '''

        def process_directory(parentNode, assignmentFilePath):

            cur1 = conn.cursor()
            global fileExtension
            userID = UserCredentials.loginUser.getUserID()
            for studentFiles in os.listdir(assignmentFilePath):
                fileExtension = re.search(r'\.\w+$', studentFiles)
                # Check if file ends with an extension, otherwise it is a folder
                abspath = os.path.join(assignmentFilePath, studentFiles)
                if fileExtension is not None:
                    isdir = os.path.isdir(abspath)
                    oid = listBox.insert(parentNode, 'end', values=(studentFiles, "", ""), open=False)
                    if isdir:
                        process_directory(oid, abspath)

                else:
                    if studentFiles == "Graded Assignments":
                        oid3 = listBox.insert(parentNode, 'end', values=(studentFiles, "", ""), open=False)
                        process_directory(oid3, abspath)

                    else:
                        try:
                            cur1.execute(
                                "SELECT SUM (final_grade) FROM assignments WHERE student_id=%s and student_id IS NOT NULL and user_id=%s and modulecode=%s and assignmentno=%s",
                                (studentFiles, userID, assignmentModuleCode, assignmentNo))
                            studentGrade = cur1.fetchall()
                            conn.commit()
                            cur1.execute(
                                "SELECT graded_status FROM assignments WHERE student_id =%s and student_id IS NOT NULL and user_id=%s and modulecode=%s and assignmentno=%s",
                                (studentFiles, userID, assignmentModuleCode, assignmentNo))
                            graded = cur1.fetchone()
                            conn.commit()
                            oid3 = listBox.insert(parentNode, 'end', values=(studentFiles, graded, studentGrade),
                                                  open=False)
                            process_directory(oid3, abspath)

                        except (psycopg2.Error, AttributeError):
                            # ToDo fix this error in postgresql transaction error, bad practice
                            conn.rollback()
                            oid3 = listBox.insert(parentNode, 'end', values=(studentFiles, "", ""),
                                                  open=False)
                            process_directory(oid3, abspath)

        def changeKeyValues():

            keysHeading_lbl = tk.Label(self, fg="black", text="Enter Values for Keys and associated comments below",
                                       font=("Calibri Bold", 14))
            keysHeading_lbl.place(x=75, y=535)

            keyA_lbl = tk.Label(self, fg="black", text="Key A: ", font=("Calibri", 12))
            keyA_lbl.place(x=75, y=565)
            keyAEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyAEntry.place(x=170, y=568)
            keyAComment_lbl = tk.Label(self, fg="black", text="Comment A: ", font=("Calibri", 12))
            keyAComment_lbl.place(x=260, y=565)
            keyACommentEntry: tk.Text = tk.Text(self, height="2", width="45")
            keyACommentEntry.place(x=350, y=568)

            keyB_lbl = tk.Label(self, fg="black", text="Key B: ", font=("Calibri", 12))
            keyB_lbl.place(x=75, y=605)
            keyBEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyBEntry.place(x=170, y=608)
            keyBComment_lbl = tk.Label(self, fg="black", text="Comment B: ", font=("Calibri", 12))
            keyBComment_lbl.place(x=260, y=605)
            keyBCommentEntry: tk.Text = tk.Text(self, height="2", width="45")
            keyBCommentEntry.place(x=350, y=608)

            keyC_lbl = tk.Label(self, fg="black", text="Key C: ", font=("Calibri", 12))
            keyC_lbl.place(x=75, y=645)
            keyCEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyCEntry.place(x=170, y=648)
            keyCComment_lbl = tk.Label(self, fg="black", text="Comment C: ", font=("Calibri", 12))
            keyCComment_lbl.place(x=260, y=645)
            keyCCommentEntry: tk.Text = tk.Text(self, height="2", width="45")
            keyCCommentEntry.place(x=350, y=648)

            keyD_lbl = tk.Label(self, fg="black", text="Key D: ", font=("Calibri", 12))
            keyD_lbl.place(x=75, y=688)
            keyDEntry: tk.Text = tk.Text(self, height="1", width="10")
            keyDEntry.place(x=170, y=692)
            keyDComment_lbl = tk.Label(self, fg="black", text="Comment D: ", font=("Calibri", 12))
            keyDComment_lbl.place(x=260, y=688)
            keyDCommentEntry: tk.Text = tk.Text(self, height="2", width="45")
            keyDCommentEntry.place(x=350, y=692)

            total_lbl = tk.Label(self, fg="black", text="Total Marks: ", font=("Calibri", 12))
            total_lbl.place(x=75, y=728)
            totalEntry: tk.Text = tk.Text(self, height="1", width="10")
            totalEntry.place(x=170, y=733)

            def saveKeysButton():
                try:
                    valueKeyA1 = int(keyAEntry.get("1.0", tk.END))
                    valueKeyB1 = int(keyBEntry.get("1.0", tk.END))
                    valueKeyC1 = int(keyCEntry.get("1.0", tk.END))
                    valueKeyD1 = int(keyDEntry.get("1.0", tk.END))
                    total = int(totalEntry.get("1.0", tk.END))
                    commentA1 = keyACommentEntry.get("1.0", 'end-1c')
                    commentB1 = keyBCommentEntry.get("1.0", 'end-1c')
                    commentC1 = keyCCommentEntry.get("1.0", 'end-1c')
                    commentD1 = keyDCommentEntry.get("1.0", 'end-1c')

                    userID = UserCredentials.loginUser.getUserID()
                    cur.execute("SELECT * FROM keysComments WHERE user_id=%s AND moduleCode = %s and assignmentNo = %s",
                                (userID, assignmentModuleCode, assignmentNo))
                    keystrokeValues = cur.fetchall()
                    conn.commit()

                    if not keystrokeValues:

                        insertKeysCommentsSQL = "INSERT INTO keysComments (user_id, moduleCode, assignmentNo, valueKeyA, commentA, valueKeyB, commentB, valueKeyC, commentC, valueKeyD, commentD, total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        keysCommentsValues = (
                            userID, assignmentModuleCode, assignmentNo, valueKeyA1, commentA1, valueKeyB1, commentB1,
                            valueKeyC1,
                            commentC1,
                            valueKeyD1, commentD1,
                            total)
                        # Executes the insertion ans passes values username and password into the insertion
                        cur.execute(insertKeysCommentsSQL, keysCommentsValues)
                        conn.commit()

                        a = int(total)
                        keysSaved_lbl = tk.Label(self, text="Values for Keys Saved", font=("Arial", 8))
                        keysSaved_lbl.place(x=320, y=525)

                    else:
                        updateKeysCommentsSQL = "UPDATE keysComments set valueKeyA = %s, commentA = %s, valueKeyB = %s, commentB = %s, valueKeyC = %s, commentC = %s, valueKeyD = %s, commentD = %s, total = %s where user_id= %s and moduleCode = %s and assignmentNo = %s"
                        keysCommentsValues = (
                            valueKeyA1, commentA1, valueKeyB1, commentB1, valueKeyC1, commentC1,
                            valueKeyD1, commentD1,
                            total, userID, assignmentModuleCode, assignmentNo)
                        # Executes the insertion ans passes values username and password into the insertion
                        cur.execute(updateKeysCommentsSQL, keysCommentsValues)
                        conn.commit()

                        a = int(total)
                        keysSaved_lbl = tk.Label(self, text="Values for Keys updated", font=("Arial", 8))
                        keysSaved_lbl.place(x=320, y=525)

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
                    changeKeyValuesButton.place(x=320, y=500)
                except ValueError:
                    keysSavedError_lbl = tk.Label(self, text="Enter values for keys", fg="red", font=("Arial", 8))
                    keysSavedError_lbl.place(x=320, y=525)

            saveButton = tk.Button(self, text="Save", width=13, command=saveKeysButton)
            saveButton.place(x=300, y=755)

        def changeValueOfAllAssignments():
            GradingFunctionality.ChangingGrades.changeStudentsGrades()

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
            listBox.place(x=75, y=220)

        lbl_title = tk.Label(self, text="Student File Selection", font=("Arial Bold", 20))
        lbl_title.place(x=400, y=35, anchor="center")

        fileAccessPath = tk.Label(self, fg="black", text="Enter File Path of Assignments: ", font=("Calibri", 12))
        fileAccessPath.place(x=75, y=110)

        filePath: tk.Entry = tk.Entry(self, width="31", font=("Calibri", 11))
        filePath.place(x=300, y=115)
        filePath.insert(0, '')

        displayAssignment = tk.Button(self, text="Display Assignments", command=getFileSelection, width=15)
        displayAssignment.place(x=530, y=114)

        clearButton = tk.Button(self, text="Clear Path", command=clearEntry, height=1, width=13)
        clearButton.place(x=660, y=114)

        moduleCode = tk.Label(self, fg="black", text="Enter Assignments Module Code: ", font=("Calibri", 12))
        moduleCode.place(x=75, y=85)

        enterModuleCode: tk.Entry = tk.Entry(self, width="12", font=("Calibri", 11))
        enterModuleCode.place(x=300, y=87)
        enterModuleCode.insert(0, '')

        assignmentNumber = tk.Label(self, fg="black", text="Assignment No.: ", font=("Calibri", 12))
        assignmentNumber.place(x=370, y=85)

        enterAssignmentNo: tk.Entry = tk.Entry(self, width="5", font=("Calibri", 11))
        enterAssignmentNo.place(x=482, y=88)
        enterAssignmentNo.insert(0, '')

        lbl_sub_title = tk.Label(self, text="List of Student Files", font=("Arial", 15))
        lbl_sub_title.place(x=380, y=180, anchor="center")

        lbl_student_files = tk.Label(self, text="Table of student files listed below", font=("Arial", 12))
        lbl_student_files.place(x=380, y=200, anchor="center")

        # Buttons at the bottom of the student file selection screen
        cannedCommentsButton = tk.Button(self, text="Canned Comments", width=15,
                                         command=GradingFunctionality.cannedComments.cannedCommentScreen)
        cannedCommentsButton.place(x=320, y=470)

        selectStudentAssignButton = tk.Button(self, text="Select Assignment", fg="black", command=fileAccess, width=15)
        selectStudentAssignButton.place(x=550, y=470)

        selectStudentAssignButton = tk.Button(self, text="Change assignments marks", fg="black",
                                              command=changeValueOfAllAssignments, width=22)
        selectStudentAssignButton.place(x=75, y=470)


def getModuleCode():
    return assignmentModuleCode


def getAssignmentNo():
    return assignmentNo


def getSelection():
    return selection


def getItem():
    return item_text


def getFilepath():
    return assignmentFilePath


if __name__ == "__main__":
    app = FileDisplayWindow()
    app.mainloop()
    the_queue.put(None)