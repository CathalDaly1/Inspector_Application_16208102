import os
import re
import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2

from DBConnection import connectToDB
from GradingFunctionality import AssignmentGrading
from UserCredentials import loginUser
from GradingAdditionalFunctionality import changingGrades, gradingCategories, cannedComments


class FileDisplayWindow(tk.Tk):
    """ This method creates the tkinter frame and window along with the elements of the tkinter window. """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.geometry("800x800+100+20")
        self.title("Inspector - Grading Application")
        self.resizable(False, False)

        frame = FileSelectionWindow(container, self)
        self.frames[FileSelectionWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(FileSelectionWindow)
        self.attributes("-topmost", 1)

    def show_frame(self, cont):
        """
        This method initializes the frame
        :param cont: cont is the FileSelectionWindow frame
        """
        frame = self.frames[cont]
        frame.tkraise()


class FileSelectionWindow(tk.Frame):
    """
    This method sets up the tkinter window with the contents of the window(labels, buttons)
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Initializing error labels
        filepathErrorLbl = tk.Label(self, text="Please enter a filepath", font=("Arial", 8), fg="red")

        conn = connectToDB.connectToDatabase()
        cur = conn.cursor()
        userID = loginUser.getUserID()

        global assignmentModuleCode, assignmentNo
        assignmentNo = ""
        assignmentModuleCode = ""

        def saveModuleCode():
            """
            Gets the module code and assignment number that are entered into the entry boxes
            :rtype: object
            """
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
            """
            Clears the entry boxes which will allow the user to re-enter data
            :rtype: object
            """
            global assignmentModuleCode, assignmentNo
            displayAssignment.config(state="active")
            cannedCommentsButton.config(state="disabled")
            categoriesButton.config(state="disabled")
            selectStudentAssignButton.config(state="disabled")
            # This clears the table when clear button is clicked
            listBox.delete(*listBox.get_children())
            assignmentNo = ""
            assignmentModuleCode = ""
            filePath.delete('0', 'end')
            enterModuleCode.delete('0', 'end')
            enterAssignmentNo.delete('0', 'end')

        def fileAccess():
            """
            Checks if the assignment No,
            :rtype: object
            """
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
                itemSelectedError_lbl = tk.Label(self, text='Please select an item from the list above', fg="red",
                                                 font=("Arial", 9))
                itemSelectedError_lbl.place(x=380, y=460, anchor="center")

        def refreshListbox():
            """
            Refreshes the data in the listbox which is being retrieved from the database.
            :rtype: object
            """
            listBox.delete(*listBox.get_children())
            assignmentPath = filePath.get()
            abspath = os.path.abspath(assignmentPath)
            root_node = listBox.insert('', 'end', text=abspath, open=True)
            process_directory(root_node, abspath)

        def onClickEvent(event):
            """
            When the user clicks on the GUI screen it will refresh the listbox
            Throw exception if the entry boxes have not been filled in
            :param event:
            :rtype: object
            """
            try:
                if assignmentNo and assignmentModuleCode != "":
                    refreshListbox()
            except NameError:
                pass

        # Bind the click event to mouse click(Left click)
        self.bind("<1>", onClickEvent)

        def doubleClickListboxEvent(event):
            """
            Gets the click of the element in the listbox in order to open file in the next window
            Throw exception if the user selects the empty row in the treeview - Index error
            :param event:
            :rtype: object
            """
            item = listBox.selection()
            try:
                for i in item:
                    global selection
                    selection = listBox.item(i, "values")[0]
            except IndexError:
                pass

        def selectAssignment():
            """
            Select assignment from the Listbox on the GUI
            Error Checking: if the file exists in the file system, if no file is selected and user selects the
            'select assignment' button
            :rtype: object
            """
            global noKeyValuesEntered_lbl, fileDoesNotExistError_lbl
            checkPath = assignmentFilePath.replace("\\", "/") + "/" + selection + "/" + str(item_text[0])

            cur.execute(
                "SELECT valueKeyA, valueKeyB,  valueKeyC, valueKeyD FROM keysComments WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
                (userID, assignmentModuleCode, assignmentNo))
            fetchedKeyValuesDisplay = cur.fetchone()
            conn.commit()

            if os.path.exists(checkPath):
                if fetchedKeyValuesDisplay is not None:
                    AssignmentGrading.selectAssignment()
                else:
                    noKeyValuesEntered_lbl = tk.Label(self, text='Enter Key values and Comments\t\t', fg="red",
                                                      font=("Arial", 9))
                    noKeyValuesEntered_lbl.place(x=440, y=745, anchor="center")
                    deleteErrorKeyValuesLabel()
            else:
                fileDoesNotExistError_lbl = tk.Label(self, text='\tFile does not exist on the file system\t\t',
                                                     fg="red",
                                                     font=("Arial", 9))
                fileDoesNotExistError_lbl.place(x=385, y=460, anchor="center")
                deleteErrorFileSelectionLabel()

        def deleteInfoLabel():
            """After 10 seconds the error label is destroyed."""
            self.after(10000, infoText_lbl.destroy)
            refreshListbox()

        def infoLabel():
            """
            Displays a label describing the correct way to select an assignment from the listbox
            This is displayed if the user incorrectly selects an assignment.
            """
            global infoText_lbl
            infoText_lbl = tk.Label(self, text="Open Assignment: Double Click Student ID.\n"
                                               "Click once on filename, click 'Select Assignment'", anchor='w',
                                    fg="red", font=("Arial", 10))
            infoText_lbl.place(x=510, y=173)
            deleteInfoLabel()

        def deleteErrorFileSelectionLabel():
            """After 10 seconds the error label is destroyed."""
            self.after(10000, fileDoesNotExistError_lbl.destroy)
            refreshListbox()

        def deleteErrorKeyValuesLabel():
            """After 10 seconds the error label is destroyed."""
            self.after(10000, noKeyValuesEntered_lbl.destroy)
            refreshListbox()

        def listboxSelection():
            """
            Get the item that has been selected and concats the string with the filepath and the filename selection
            In order open the file; the full filepath and the name of the file must be selected
            :rtype: object
            """
            # Check if the filepath has been entered
            if filePath.get() != "":
                global item_text

                for item in listBox.selection():
                    item_text = listBox.item(item, "values")

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
                                                            "Do you want to regrade this assignment?", parent=self)

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

        def getFileSelection():
            """
            Check of filepath has been entered and if it exists or not
            if the directory exists then folders and files are displayed in the listbox
            Displayed also is the status of the assignment grading = Y or N and the grade = 'Int
            :rtype: object
            """
            saveModuleCode()
            global assignmentFilePath
            assignmentFilePath = filePath.get()

            # Check if the entered filepath exists on the users file system
            if os.path.exists(assignmentFilePath) and assignmentModuleCode and assignmentNo != "":
                directoryExists_lbl = tk.Label(self, text="\tDirectory Exists\t\t\t", font=("Calibri", 9))
                directoryExists_lbl.place(x=300, y=142)

                root_node = listBox.insert('', 'end', text=assignmentFilePath, open=True)
                process_directory(root_node, assignmentFilePath)

                cur.execute(
                    "SELECT * FROM keyscomments WHERE user_id =%s and modulecode = %s and assignmentno = %s",
                    (userID, assignmentModuleCode, assignmentNo))
                keystrokes = cur.fetchone()
                conn.commit()

                #  Disable button after it has been clicked once in order for the data to only appear once
                displayAssignment.config(state="disabled")
                #  Enable buttons after it has been clicked once in order for the data to only appear once
                cannedCommentsButton.config(state="active")
                categoriesButton.config(state="active")
                selectStudentAssignButton.config(state="active")

                if keystrokes is None:
                    changeKeyValues()
                else:
                    changeKeyValuesButton = tk.Button(self, text="Change Keys values", width=15,
                                                      command=changeKeyValues)
                    changeKeyValuesButton.place(x=320, y=500)

                listBox.bind("<Double-Button-1>", doubleClickListboxEvent)

            else:
                moduleCodeSaved_lbl = tk.Label(self, text="Please enter the Module Code and Assignment No.\t\t",
                                               fg="red")
                moduleCodeSaved_lbl.place(x=527, y=85)
                directoryErrorLbl = tk.Label(self, text="Ensure Entry boxes are filled in and correct",
                                             font=("Calibri", 9), fg="red")
                directoryErrorLbl.place(x=298, y=142)

        def process_directory(parentNode, assignmentFilePath):
            """
            Checks if file is in the directory, adds other columns if it is a file
            display data from the database into the to treeview
            :rtype: object
            """
            global fileExtension

            for studentFiles in os.listdir(assignmentFilePath):

                fileExtension = re.search(r'\.\w+$', studentFiles)
                abspath = os.path.join(assignmentFilePath, studentFiles)

                # Check if file ends with an extension, otherwise it is a folder
                if fileExtension is not None:
                    listBox.insert(parentNode, 'end', values=(studentFiles, "", ""), open=False)

                elif studentFiles == "Graded Assignments":
                    pass

                else:
                    try:
                        cur.execute(
                            "SELECT SUM (final_grade) FROM assignments WHERE student_id=%s and student_id IS NOT NULL "
                            "and user_id=%s and modulecode=%s and assignmentno=%s",
                            (studentFiles, userID, assignmentModuleCode, assignmentNo))
                        studentGrade = cur.fetchone()

                        cur.execute(
                            "SELECT graded_status FROM assignments WHERE student_id =%s and student_id IS NOT NULL"
                            " and user_id=%s and modulecode=%s and assignmentno=%s",
                            (studentFiles, userID, assignmentModuleCode, assignmentNo))
                        graded = cur.fetchone()

                        listBoxStudentAssignmentData = listBox.insert(parentNode, 'end', values=(studentFiles,
                                                                                                 graded,
                                                                                                 studentGrade),
                                                                      open=False)

                        process_directory(listBoxStudentAssignmentData, abspath)
                        conn.commit()
                    except Exception:
                        conn.rollback()

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

            total_lbl = tk.Label(self, fg="black", text="Initial Marks: ", font=("Calibri", 12))
            total_lbl.place(x=75, y=728)
            totalEntry: tk.Text = tk.Text(self, height="1", width="10")
            totalEntry.place(x=170, y=733)

            def saveKeysButton():
                """
                Saves the values and comments that have been entered into the entry boxes for the key values and the
                comments. These key values and comments are then entered into the database.
                :rtype: object
                """
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

                        keysSaved_lbl = tk.Label(self, text="Values for Keys updated", font=("Arial", 8))
                        keysSaved_lbl.place(x=320, y=523)

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
                    keysSavedError_lbl = tk.Label(self, text="Enter values for keys\t", fg="red", font=("Arial", 8))
                    keysSavedError_lbl.place(x=320, y=525)

            saveButton = tk.Button(self, text="Save", width=13, command=saveKeysButton)
            saveButton.place(x=300, y=755)

        def changeValueOfAllAssignments():
            """
            This method calls the change student grade method in th changingGrades file
            This method is called when the 'Change assignments marks' button is pressed.
            """
            changingGrades.changeStudentsGrades()

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
        lbl_sub_title.place(x=380, y=200, anchor="center")

        # Buttons at the bottom of the student file selection screen
        cannedCommentsButton = tk.Button(self, text="Canned Comments", width=15,
                                         command=cannedComments.cannedCommentScreen)
        cannedCommentsButton.place(x=320, y=470)

        selectStudentAssignButton = tk.Button(self, text="Select Assignment", fg="black", command=fileAccess, width=15)
        selectStudentAssignButton.place(x=562, y=470)

        selectStudentAssignButton = tk.Button(self, text="Change assignments marks", fg="black",
                                              command=changeValueOfAllAssignments, width=22)
        selectStudentAssignButton.place(x=75, y=470)

        categoriesButton = tk.Button(self, text="Add grading categories", width=22,
                                     command=gradingCategories.gradingCategoriesScreen)
        categoriesButton.place(x=75, y=500)

        cannedCommentsButton.config(state="disabled")
        categoriesButton.config(state="disabled")
        selectStudentAssignButton.config(state="disabled")


def getModuleCode():
    """
    Get the module code that has been entered into the module code entry box
    :return: assignment module code from the entry box
    """
    return assignmentModuleCode


def getAssignmentNo():
    """
    Get the assignment number that has been entered into the Assigment No. entry box
    :return: Assignment No. from the entry box
    """
    return assignmentNo


def getSelection():
    """
    get the filename that has been selected in the listbox
    :return: filename from the listbox selection
    """
    return selection


def getItem():
    """
    get the folder name that has been double clicked in the listbox
    :return: folder name from the listbox when double clicked
    """
    return item_text


def getFilepath():
    """
    Get the filepath that has been entered into the Assignment FilePath entry box
    :return: filepath from the entry box
    """
    return assignmentFilePath


if __name__ == "__main__":
    app = FileDisplayWindow()
    app.mainloop()
