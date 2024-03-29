import functools
import operator
import tkinter as tk
from tkinter import ttk

from gevent._compat import izip
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import xlsxwriter
from xlsxwriter.exceptions import FileCreateError

from DBConnection import connectToDB
from UserCredentials import loginUser

style.use('fivethirtyeight')

conn = connectToDB.connectToDatabase()
cur = conn.cursor()


def analyticsScreen():
    """
    Analytics screen allows the user to filter via module code and assignment number
    They can then view the assignments graded and the students details. A bar graph is
    also displayed showing the distribution of grades for that assignment. The user can
    also export the data in the table into a CSV file if they wish.
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("850x800+100+20")
    window.resizable(False, False)

    userID = loginUser.getUserID()
    cur.execute("SELECT count(*) FROM assignments WHERE user_id =%s",
                (userID,))
    number = cur.fetchone()
    num = int(number[0])
    conn.commit()

    lbl_title = tk.Label(window, text="Inspector - Grading Analysis", font=("Arial Bold", 18))
    lbl_title.place(x=400, y=50, anchor="center")

    numberOfAssignmentsGraded_lbl = tk.Label(window, fg="black", text="Number of Assignments graded: " + str(num),
                                             font=("Calibri", 14))
    numberOfAssignmentsGraded_lbl.place(x=25, y=70)

    cols = ('Student ID', 'Filename', 'Student Grade', 'Date/Time Graded')
    listBox = ttk.Treeview(window, selectmode="extended", columns=cols, show='headings')

    # Added scrollbar onto the listbox
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=listBox.yview)
    listBox['yscroll'] = scrollbar.set

    scrollbar.place(in_=listBox, relx=1.0, relheight=1.0, bordermode="outside")

    for col in cols:
        listBox.heading(col, text=col)
        listBox.place(x=25, y=160)

    label_module = tk.Label(window, text="Choose module from list: ", font=("Calibri", 14))
    label_module.place(x=25, y=95)

    # As there are duplicates of assignments with module codes have to use distinct
    cur.execute("SELECT DISTINCT modulecode FROM assignments WHERE user_id =%s",
                (userID,))
    moduleCode = cur.fetchall()
    conn.commit()

    moduleCombobox = ttk.Combobox(window, values=moduleCode)
    moduleCombobox.place(x=230, y=100)

    def displayAssignment():
        """
        This method is called the display assignment button is pressed.
        """
        assignmentCombobox()

    def refreshTable():
        """
        This method refreshes the tkinter table(treeview) and it is called when a new search is made.
        """
        listBox.delete(*listBox.get_children())

    def assignmentCombobox():
        """
        This method allows the user to choose a module code and also an assignment to filter.
        """
        global moduleCodeSelection
        global assignmentSelection
        global assignmentCombo
        moduleCodeSelection = moduleCombobox.get()
        label_assignment = tk.Label(window, text="Choose Assignment No.: ", font=("Calibri", 14))
        label_assignment.place(x=25, y=125)

        # As there are duplicates of assignments with module codes have to use distinct
        cur.execute("SELECT DISTINCT assignmentNo FROM assignments WHERE user_id =%s and moduleCode = %s",
                    (userID, moduleCodeSelection))
        assignmentSelection = cur.fetchall()
        conn.commit()

        assignmentCombo = ttk.Combobox(window, values=assignmentSelection)
        assignmentCombo.place(x=230, y=130)

        saveAssignmentSelection = tk.Button(window, text="Display Table", fg="black", command=showTable, width=15)
        saveAssignmentSelection.place(x=400, y=127)

    def displayModuleAssignments():
        """
        This method displays the data in the table and also generates the bar chart. Data is retrieved from the
        database assignments table. The data displayed in the bar chart is the final grade that each student
        received. As there may be more than one file graded per assignment submission, there is a for loop that
        retrieves the final grades of the students in the database and gets the sum of each individually graded
        assignment. This sum is then displayed in the bar chart.
        :rtype: object
        """
        if assignmentSelect != "":
            refreshTable()
            exportData_Button.config(state="active")
            cur.execute("SELECT student_id, filename, final_grade, time_graded FROM assignments WHERE user_id =%s and modulecode=%s and assignmentno = %s",
                        (userID, moduleCodeSelection, assignmentSelect))

            assignmentData = cur.fetchall()
            conn.commit()

            for row in assignmentData:
                listBox.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

            cur.execute(
                "SELECT DISTINCT student_id from assignments where user_id=%s and modulecode=%s and assignmentno=%s",
                (userID, moduleCodeSelection, assignmentSelect))
            studentID = cur.fetchall()
            conn.commit()

            studentIdList = [item for t in studentID for item in t]
            numberOfGradedAssignments = []
            grade = []

            # Loop through list of student ID numbers, retrieving their final grade(s) for the files that they submitted
            # The sum of each of the graded file submissions is added and displayed in the bar chart.
            for a in zip(studentIdList):
                cur.execute(
                    "SELECT final_grade from assignments where user_id=%s and modulecode=%s and assignmentno=%s and student_id=%s",
                    (userID, moduleCodeSelection, assignmentSelect, a))
                studentFinalGrade = cur.fetchall()
                sumOfGrades = [sum(x) for x in izip(*studentFinalGrade)]

                numberOfGradedAssignments.append(len(grade))
                grade.append(sumOfGrades[0])

                figure1 = Figure(figsize=(6, 4), dpi=80)
                subplot1 = figure1.add_subplot(111)
                xAxis = numberOfGradedAssignments
                yAxis = grade
                subplot1.bar(xAxis, yAxis, color='lightsteelblue')
                bar1 = FigureCanvasTkAgg(figure1, window)
                bar1.get_tk_widget().place(x=150, y=390)
                subplot1.set_title('Grade Distribution for ' + str(moduleCodeSelection))

    def showTable():
        """
        This method calls the displayModuleAssignments method.
        """
        global moduleCodeSelection
        global assignmentSelect
        moduleCodeSelection = moduleCombobox.get()
        assignmentSelect = assignmentCombo.get()
        displayModuleAssignments()

    def convertTuple(pathTuple):
        convertTup = functools.reduce(operator.add, pathTuple)
        return convertTup

    def exportData():
        """
        This method is called when the 'export data' button is pressed. Exports data from table into an
        excel file. Throw exception if the excel file is unable to be saved. This may primarily be as
        a result of the file being opened on the users machine.
        :rtype: object
        """

        cur.execute(
            "SELECT DISTINCT filepath FROM assignments WHERE user_id =%s and modulecode=%s and assignmentno=%s",
            (userID, moduleCodeSelection, assignmentSelect))
        getFilepath = cur.fetchone()

        conn.commit()

        studentAssignmentFilePathTuple = convertTuple(getFilepath[0])
        studentAssignmentFilePath = studentAssignmentFilePathTuple.replace("\\", "/")

        workbook = xlsxwriter.Workbook(studentAssignmentFilePath + "/"
                                       + moduleCodeSelection + "-" + assignmentSelect + '.xlsx')
        worksheet = workbook.add_worksheet()

        # Formatting the excel file when it is exported
        format1 = workbook.add_format({'num_format': 'mmm d yyyy hh:mm:ss'})
        worksheet.set_column('C:C', 11)
        worksheet.set_column('D:D', 11)
        worksheet.set_column('F:F', 20, format1)
        worksheet.set_column('G:G', 51)
        worksheet.autofilter('A1:G200')

        cur.execute("SELECT modulecode, assignmentno, student_id, filename, final_grade, time_graded, filepath FROM assignments WHERE user_id =%s and modulecode=%s and assignmentno=%s",
                    (userID, moduleCodeSelection, assignmentSelect))
        assignmentData = cur.fetchall()

        try:
            # Writes the headings from the DB table into the xls file
            for column, heading in enumerate(cur.description):
                # first element of each tuple
                worksheet.write(0, column, heading[0])

            # Writes the rows in the DB table into the xls file
            for rows, row in enumerate(assignmentData):
                for colindex, col in enumerate(row):
                    worksheet.write(rows + 1, colindex, col)
            workbook.close()

            print("File location of exported data: " + studentAssignmentFilePath + '/ExportedCSVFiles/')

            exportDataConfirmed_lbl = tk.Label(window, text="Data Exported to " + moduleCodeSelection + " file location"
                                               , font=("Calibri", 12))
            exportDataConfirmed_lbl.place(x=550, y=125)

        except FileCreateError as error:
            print(str(error))
            exportDataConfirmed_lbl = tk.Label(window, text="Error saving file\t\t\t", fg="red", font=("Calibri", 12))
            exportDataConfirmed_lbl.place(x=550, y=125)

    def back():
        """
        This method is called when the back button is pressed. Window is destroyed.
        """
        window.destroy()

    exportData_lbl = tk.Label(window, text="Export Data - CSV ", font=("Calibri", 14))
    exportData_lbl.place(x=550, y=95)

    exportData_Button = tk.Button(window, text="Export", fg="black", command=exportData, width=15)
    exportData_Button.place(x=700, y=95)
    exportData_Button.config(state="disabled")

    saveModuleSelection = tk.Button(window, text="Display Assignments", fg="black", command=displayAssignment, width=15)
    saveModuleSelection.place(x=400, y=100)

    back_button = tk.Button(window, text="Back", fg="black", command=back, height=2, width=12)
    back_button.place(x=350, y=730)
