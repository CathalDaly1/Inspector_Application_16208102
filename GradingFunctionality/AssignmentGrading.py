import datetime
import os
import queue
import re
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import fitz
from fpdf import FPDF

import UserCredentials.loginUser
import DBConnection.connectToDB
import GradingFunctionality.AccessingFiles
import MenuOptions.commandsMenu

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()

the_queue = queue.Queue()


def selectAssignment():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("1200x985+50+50")
    window.resizable(False, False)

    menubar = tk.Menu(window)

    userID = UserCredentials.loginUser.getUserID()
    assignmentModuleCode = GradingFunctionality.AccessingFiles.getModuleCode()
    assignmentNo = GradingFunctionality.AccessingFiles.getAssignmentNo()
    selection = GradingFunctionality.AccessingFiles.getSelection()
    item_text = GradingFunctionality.AccessingFiles.getItem()
    filePath = GradingFunctionality.AccessingFiles.getFilepath()

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = Path(ROOT_DIR)
    # Get the parent folder of the project
    parentPath = str(path.parent)
    # Replace the \\ in the filepath with / in order for the application to be able to save the file
    correctParentPath = (parentPath.replace("\\", "/"))
    fileHighlightText = (str(correctParentPath) + "/HighlightFiles/highlightedText.txt")
    open(fileHighlightText, 'w').close()

    global file
    global gradedFilesFolder
    fileExtensionSelection = re.search(r'\.\w+$', selection)
    # Get the click event of the selection from the listbox, use that selection to create a new filepath and add new graded files
    gradedFilesFolder = filePath.replace("\\", "/") + "/" + "Graded Assignments" + "/" + selection + "/"
    if not os.path.exists(gradedFilesFolder):
        os.makedirs(gradedFilesFolder)

    # Check if listbox selection is a filename or a folder
    # If it is a filename, concat the string of the filepath and the filename
    if fileExtensionSelection is not None:
        file = filePath.replace("\\", "/") + "/" + str(item_text[0])

    # If it is a folder, concat the string of the filepath, the folder and the selection
    else:
        # Get the filename and remove the \t tab which is needed to display listbox with indentation
        file = filePath.replace("\\", "/") + "/" + selection + "/" + str(item_text[0])
        # file = re.sub('\t', '', file)

    # Menubar in the top left of the screen
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="View Keystrokes", command=MenuOptions.commandsMenu.menuOptions)
    # file_menu.add_command(label="View Canned Comments", command=viewCannedComments)
    file_menu.add_separator()
    file_menu.add_command(label="Quit Inspector", command=quit)
    menubar.add_cascade(label="File", menu=file_menu)

    helpMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpMenu)

    # display the menu
    window.config(menu=menubar)

    def startGrading(event):
        window.unbind("<s>", bind_id)
        userID = UserCredentials.loginUser.getUserID()
        cur.execute(
            "SELECT comment1, comment2, comment3, comment4, comment5 FROM cannedComments WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
            (userID, assignmentModuleCode, assignmentNo))
        fetchedComments = cur.fetchone()

        cur.execute(
            "SELECT valueKeyA, commentA, valueKeyB, commentB, valueKeyC, commentC, valueKeyD, commentD, total FROM keysComments WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
            (userID, assignmentModuleCode, assignmentNo))
        fetchedKeyValues = cur.fetchone()
        conn.commit()

        cur.execute(
            "SELECT categoryA, categoryB, categoryC, categoryD, categoryE FROM gradingCategories WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
            (userID, assignmentModuleCode, assignmentNo))
        fetchedCategories = cur.fetchone()

        global total1
        total1 = fetchedKeyValues[8]
        valueKeyA = fetchedKeyValues[0]
        commentA = fetchedKeyValues[1]
        valueKeyB = fetchedKeyValues[2]
        commentB = fetchedKeyValues[3]
        valueKeyC = fetchedKeyValues[4]
        commentC = fetchedKeyValues[5]
        valueKeyD = fetchedKeyValues[6]
        commentD = fetchedKeyValues[7]
        a = total1

        the_queue.put("Grading has started - Total marks: " + str(total1))

        def keyA(event):
            global total1
            total1 += valueKeyA
            the_queue.put("Awarded " + str(valueKeyA) + " marks\n" + str(total1) + " marks - " + commentA)

        def keyB(event):
            global total1
            total1 += valueKeyB
            the_queue.put("Awarded " + str(valueKeyB) + " marks\n" + str(total1) + " marks - " + commentB)

        def keyC(event):
            global total1
            total1 += valueKeyC
            the_queue.put("Awarded " + str(valueKeyC) + " marks\n" + str(total1) + " marks - " + commentC)

        def keyD(event):
            global total1
            total1 += valueKeyD
            the_queue.put("Awarded " + str(valueKeyD) + " marks\n" + str(total1) + " marks - " + commentD)

        def keyE(event):
            global total1
            global final
            the_queue.put("Final Grade: " + str(total1) + " marks")
            # sets the total to the initial value again
            final = total1
            total1 = a
            the_queue.empty()

        def cannedComment1(event):
            try:
                comment1 = fetchedComments[0]
                the_queue.put("Comment 1: " + str(comment1))
            except TypeError as error:
                the_queue.put("You have not added a comment for Key 1")
                print("Comment 1:" + str(error))

        def cannedComment2(event):
            try:
                comment2 = fetchedComments[1]
                the_queue.put("Comment 1: " + str(comment2))
            except TypeError as error:
                the_queue.put("You have not added a comment for Key 2")
                print("Comment 2:" + str(error))

        def cannedComment3(event):
            try:
                comment3 = fetchedComments[2]

                the_queue.put("Comment 1: " + str(comment3))
            except TypeError as error:
                the_queue.put("You have not added a comment for Key 3")
                print("Comment 3:" + str(error))

        def cannedComment4(event):
            try:
                comment4 = fetchedComments[3]
                the_queue.put("Comment 1: " + str(comment4))
            except TypeError as error:
                the_queue.put("You have not added a comment for Key 4")
                print("Comment 4:" + str(error))

        def cannedComment5(event):
            try:
                comment5 = fetchedComments[4]
                the_queue.put("Comment 1: " + str(comment5))
            except TypeError as error:
                the_queue.put("You have not added a comment for Key 5")
                print("Comment 5:" + str(error))

        def gradingCategoryA(event):
            try:
                categoryA = fetchedCategories[0]
                the_queue.put("Category: " + str(categoryA))
            except TypeError as error:
                the_queue.put("You have not added category A")
                print("Category A:" + str(error))

        def gradingCategoryB(event):
            try:
                categoryB = fetchedCategories[1]
                the_queue.put("Category: " + str(categoryB))
            except TypeError as error:
                the_queue.put("You have not added category B")
                print("Category B:" + str(error))

        def gradingCategoryC(event):
            try:
                categoryC = fetchedCategories[2]
                the_queue.put("Category: " + str(categoryC))
            except TypeError as error:
                the_queue.put("You have not added category C")
                print("Category C:" + str(error))

        def gradingCategoryD(event):
            try:
                categoryD = fetchedCategories[3]
                the_queue.put("Category: " + str(categoryD))
            except TypeError as error:
                the_queue.put("You have not added category D")
                print("Category D:" + str(error))

        def gradingCategoryE(event):
            try:
                categoryE = fetchedCategories[4]
                the_queue.put("Category: " + str(categoryE))
            except TypeError as error:
                the_queue.put("You have not added category E")
                print("Category E:" + str(error))

        keystrokeGrading.bind('a', keyA) and keystrokeGrading.bind("<A>", keyA)
        keystrokeGrading.bind('b', keyB) and keystrokeGrading.bind("<B>", keyB)
        keystrokeGrading.bind('c', keyC) and keystrokeGrading.bind("<C>", keyC)
        keystrokeGrading.bind('d', keyD) and keystrokeGrading.bind("<D>", keyD)
        keystrokeGrading.bind('e', keyE) and keystrokeGrading.bind("<E>", keyE)
        keystrokeGrading.bind('1', cannedComment1)
        keystrokeGrading.bind('2', cannedComment2)
        keystrokeGrading.bind('3', cannedComment3)
        keystrokeGrading.bind('4', cannedComment4)
        keystrokeGrading.bind('5', cannedComment5)
        keystrokeGrading.bind('<Control-a>', gradingCategoryA) and keystrokeGrading.bind('<Control-A>',
                                                                                         gradingCategoryA)
        keystrokeGrading.bind('<Control-b>', gradingCategoryB) and keystrokeGrading.bind('<Control-B>',
                                                                                         gradingCategoryB)
        keystrokeGrading.bind('<Control-c>', gradingCategoryC) and keystrokeGrading.bind('<Control-C>',
                                                                                         gradingCategoryC)
        keystrokeGrading.bind('<Control-d>', gradingCategoryD) and keystrokeGrading.bind('<Control-D>',
                                                                                         gradingCategoryD)
        keystrokeGrading.bind('<Control-e>', gradingCategoryE) and keystrokeGrading.bind('<Control-E>',
                                                                                         gradingCategoryE)

    window.bind('s', startGrading)
    bind_id = window.bind("<s>", startGrading)

    def queue_callback():
        try:
            message = the_queue.get(block=False)

        except queue.Empty:
            # retry
            window.after(100, queue_callback)
            return

        if message is not None:
            # Print out the message once there is something in the queue
            studentFinalGrade['text'] = message
            # Insert messages from the queue into the text box
            GradeTextBox.insert(tk.END, message + "\n")
            # Scroll to the end of text when new text is added
            GradeTextBox.see("end")
            window.after(100, queue_callback)

    # Start the thread and run the keystrokeApplication_thread function
    # thread = threading.Thread(target=keystrokeApplication_thread)
    # thread.start()
    window.after(100, queue_callback)

    assign_correction_lbl = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
    assign_correction_lbl.place(x=400, y=26, anchor="center")

    subTitle_lbl = tk.Label(window, text="Student: " + selection + "'s Assignment", font=("Arial", 15))
    subTitle_lbl.place(x=400, y=70, anchor="center")

    userID = UserCredentials.loginUser.getUserID()
    cur.execute(
        "SELECT valueKeyA, valueKeyB,  valueKeyC, valueKeyD FROM keysComments WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
        (userID, assignmentModuleCode, assignmentNo))
    fetchedKeyValuesDisplay = cur.fetchone()
    conn.commit()

    valueKeyADisplay = fetchedKeyValuesDisplay[0]
    valueKeyBDisplay = fetchedKeyValuesDisplay[1]
    valueKeyCDisplay = fetchedKeyValuesDisplay[2]
    valueKeyDDisplay = fetchedKeyValuesDisplay[3]

    keystrokes_lbl = tk.Label(window, width=47, height=27, relief="solid", bd=1, padx=10, bg="white")
    keystrokes_lbl.pack_propagate(0)
    keystrokes_lbl.place(x=790, y=95)
    tk.Label(keystrokes_lbl, bg="white", fg="black", text="Key Shortcuts", font=("Calibri Bold", 18)).pack()
    tk.Label(keystrokes_lbl, bg="white", justify=tk.LEFT,
             text="View detailed keystrokes: File->View Keystrokes" + "\n" + "Key S: Start Grading" + "\n"
                  + "Ctrl + S: Submit Assignment" + "\n" + "Ctrl + R: Highlight Text\n"
                  + "Key A: +" + str(valueKeyADisplay) + " - Comment A \n" + "Key B: +" +
                  str(valueKeyBDisplay) + " - Comment B \n" + "Key C: + " +
                  str(valueKeyCDisplay) + " - Comment C \n" + "Key D: + " +
                  str(valueKeyDDisplay) + " - Comment D \n"
                  + "Key E: Finish grading\n"
                  +
                  "Canned Comment 1: Key 1\n"
                  +
                  "Canned Comment 2: Key 2\n"
                  +
                  "Canned Comment 3: Key 3\n"
                  +
                  "Canned Comment 4: Key 4\n"
                  +
                  "Canned Comment 5: Key 5\n"
                  +
                  "Category A: Ctrl + A\n"
                  +
                  "Category B: Ctrl + B\n"
                  +
                  "Category C: Ctrl + C\n"
                  +
                  "Category D: Ctrl + D\n"
                  +
                  "Category E: Ctrl + E\n", wraplengt=345, font=("Arial", 12)).pack()

    studentFinalGrade = tk.Label(window, wraplengt=350, font=("Arial", 12))
    studentFinalGrade.place(x=790, y=570)

    keystrokeGrading_lbl = tk.Label(window, text="Enter keystroke selections below", font=("Arial", 12))
    keystrokeGrading_lbl.place(x=790, y=520)

    keystrokeGrading: tk.Text = tk.Text(window, height="1", width="27", font=("Calibri", 12))
    keystrokeGrading.place(x=792, y=540)

    GradeTextBox = tk.Text(window, wrap=tk.NONE, height=10, width=90, borderwidth=0)
    GradeTextBox.place(x=45, y=730)

    # Scrollbar on X and Y axis of GradeTextBox
    GradeTextBoxScrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=GradeTextBox.yview)
    GradeTextBox['yscroll'] = GradeTextBoxScrollbar.set
    GradeTextBox.insert(tk.END, "***Grade/Comments***\n")

    GradeTextBoxScrollbar.place(in_=GradeTextBox, relx=1.0, relheight=1.0, bordermode="outside")

    # Opens the file and copies the contents into the text box for editing
    global assignment
    try:
        assignment = open(file, encoding="ISO-8859-1").read()
    except FileNotFoundError:
        print("Implement this please")

    def highlightingTextInFile():
        savingFilePDF = re.sub('\t', '', item_text[0] + ".pdf")
        doc = fitz.open(gradedFilesFolder + "\\" + savingFilePDF)
        print(str(gradedFilesFolder + "\\" + savingFilePDF))
        page = doc[0]

        with open(fileHighlightText, "r") as file2:
            time.sleep(0.5)
            text1 = file2.read()
        text_instances = page.searchFor(text1, hit_max=50)

        for inst in text_instances:
            print(inst, type(inst))
            highlight = page.addHighlightAnnot(inst)

        try:
            doc.save(gradedFilesFolder + "\\" + "Corrected - " + savingFilePDF,
                     garbage=4, deflate=True, clean=True)
            doc.close()
            os.remove(gradedFilesFolder + "\\" + savingFilePDF)

        except RuntimeError:
            print("PDF file may be open")

    class TextLineNumbers(tk.Canvas):

        def __init__(self, *args, **kwargs):
            tk.Canvas.__init__(self, *args, **kwargs)
            self.textwidget = None

        def attach(self, text_widget):
            self.textwidget = text_widget

        def redraw(self, *args):
            '''redraw line numbers '''
            self.delete("all")

            i = self.textwidget.index("@0,0")
            while True:
                dline = self.textwidget.dlineinfo(i)
                if dline is None: break
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.create_text(2, y, anchor="nw", text=linenum)
                i = self.textwidget.index("%s+1line" % i)

    class generatingLineNumbersLive(tk.Text):
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

    class lineNumbers(tk.Frame):
        def __init__(self, *args, **kwargs):
            tk.Frame.__init__(self, *args, **kwargs)
            self.text = generatingLineNumbersLive(self, width=84, wrap=tk.NONE, height=35)
            self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
            self.codeLineNumbers = TextLineNumbers(self, width=30, bg="deep sky blue")
            self.codeLineNumbers.attach(self.text)

            self.codeLineNumbers.pack(side="left", fill="y")
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

            window.bind("<Control-S>", lambda event: self.submitAssignment(event))
            window.bind("<Control-s>", lambda event: self.submitAssignment(event))
            window.bind("<Escape>", lambda event: self.back(event))
            window.bind("<Control-r>", lambda event: self.highlightCode(event))
            window.bind("<Control-R>", lambda event: self.highlightCode(event))
            window.protocol("WM_DELETE_WINDOW", self.on_closingWindow)

        def _on_change(self, event):
            self.codeLineNumbers.redraw()

        def testPrint(self, event):
            print("check")

        def savePDFFile(self):
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
            pdf.output(gradedFilesFolder + "\\" + savingFilePDF)
            highlightingTextInFile()

        def submitAssignment(self, _event=None):
            userIDNo = UserCredentials.loginUser.getUserID()
            assignmentFilePath = GradingFunctionality.AccessingFiles.getFilepath()
            cur.execute(
                "SELECT * FROM assignments WHERE user_id =%s and student_id = %s and filename = %s and moduleCode = %s",
                (userID, selection, item_text[0], assignmentModuleCode))
            vals = cur.fetchone()
            print(vals)
            conn.commit()

            if vals is not None:
                if str(vals[1]) == str(userID) and str(vals[4]) == str(selection) and str(vals[5]) == str(
                        item_text[0]):
                    try:
                        cur.execute(
                            "Update assignments set final_grade = %s where user_id =%s and modulecode = %s and student_id = %s and filename = %s",
                            (final, userID, assignmentModuleCode, selection, item_text[0],))
                        conn.commit()

                        window.withdraw()
                        self.savePDFFile()

                    except NameError:
                        messagebox.showwarning(title="Inspector - Grading application",
                                               message="You have not finished grading")
            else:
                try:
                    time_graded = datetime.datetime.now()
                    insertAssignments = "INSERT INTO assignments (user_id, modulecode, assignmentNo, student_id, filename, final_grade, graded_status, time_graded, filepath) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    assignmentValues = (
                        userIDNo, assignmentModuleCode, assignmentNo, selection, item_text[0], final, 'Y',
                        time_graded, assignmentFilePath)
                    # Executes the insertion ans passes values username and password into the insertion
                    cur.execute(insertAssignments, assignmentValues)
                    conn.commit()

                    window.withdraw()
                    self.savePDFFile()

                except NameError:
                    messagebox.showwarning(title="Inspector - Grading application",
                                           message="You have not finished grading")

        # Highlights code and text when text is selected and highlight button is pressed
        def highlightCode(self, _event=None):
            count = 0
            if self.text.tag_ranges('sel'):
                self.text.tag_add('color' + str(count), tk.SEL_FIRST, tk.SEL_LAST)
                self.text.tag_configure('color' + str(count), foreground='black', background='yellow')
                count += 1
            else:
                # Do this if you want to overwrite all selection colors when you change color without selection
                # for tag in text.tag_names():
                #     text.tag_delete(tag)
                self.text.config(foreground='yellow')

            fileContainingText = open(fileHighlightText, "a")

            hText = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            fileContainingText.write(hText)

        def addAssignmentComments(self, _event=None):
            self.text.insert(tk.END, "\n")
            self.text.insert(tk.INSERT, GradeTextBox.get("1.0", "end-1c"))

        # If window is closed mid grading, save the file in the folder
        def on_closingWindow(self):
            if messagebox.askokcancel("Quit",
                                      "Do you want to quit grading the assignment?\n File will be saved"):
                self.submitAssignment()

        def back(self, _event=None):
            # Clears listbox when returning to the file selection screen: this is in order to reselect the path
            # Call on_closingwindow() to save assignment if backbutton is pressed
            self.on_closingWindow()

    lineNumbers(window).place(x=60, y=95)
