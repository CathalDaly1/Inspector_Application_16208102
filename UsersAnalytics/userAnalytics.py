import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import xlsxwriter
from xlsxwriter.exceptions import FileCreateError

import DBConnection.connectToDB
import UserCredentials.loginUser

style.use('fivethirtyeight')

conn = DBConnection.connectToDB.connectToDB()
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
    window.geometry("850x800+100+100")
    window.resizable(False, False)

    userID = UserCredentials.loginUser.getUserID()
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
        database assignments table.
        """
        if assignmentSelect != "":
            refreshTable()
            exportData_Button.config(state="active")
            cur.execute("SELECT * FROM assignments WHERE user_id =%s and modulecode=%s and assignmentno = %s",
                        (userID, moduleCodeSelection, assignmentSelect))

            assignmentData = cur.fetchall()
            conn.commit()

            for row in assignmentData:
                listBox.insert("", tk.END, values=(row[4], row[5], row[6], row[8]))

            numberOfGradedAssignments = []
            grade = []

            for row1 in assignmentData:
                # x axis is the number of assignments graded in order to graph them
                numberOfGradedAssignments.append(len(grade))
                grade.append(row1[6])

                figure1 = Figure(figsize=(6, 4), dpi=80)
                subplot1 = figure1.add_subplot(111)
                xAxis = numberOfGradedAssignments
                yAxis = grade
                subplot1.bar(xAxis, yAxis, color='lightsteelblue')
                bar1 = FigureCanvasTkAgg(figure1, window)
                bar1.get_tk_widget().place(x=150, y=390)
                subplot1.set_title('Grade Distribution for ' + str(moduleCodeSelection))
                assignmentNo_lbl = tk.Label(window, text="Assignment data has been displayed. ", fg="black",
                                            font=("Calibri", 12))
                assignmentNo_lbl.place(x=550, y=130)
        else:
            assignmentNo_errorlbl = tk.Label(window, text="Please enter an assignment No. ", fg="red", font=("Calibri", 12))
            assignmentNo_errorlbl.place(x=550, y=130)

    def showTable():
        """
        This method calls the displayModuleAssignments method.
        """
        global moduleCodeSelection
        global assignmentSelect
        moduleCodeSelection = moduleCombobox.get()
        assignmentSelect = assignmentCombo.get()
        displayModuleAssignments()

    def exportData():
        """
        This method is called when the 'export data' button is pressed. Exports data from table into an
        excel file.
        """
        cur.execute("SELECT modulecode, assignmentno, student_id, filename, final_grade, time_graded, filepath FROM assignments WHERE user_id =%s and modulecode=%s and assignmentno=%s",
                    (userID, moduleCodeSelection, assignmentSelect))

        assignmentData = cur.fetchall()
        conn.commit()
        # Get the root directory of the project in the users machine
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        path = Path(ROOT_DIR)
        # Get the parent folder of the project
        parentPath = str(path.parent)
        # Replace the \\ in the filepath with / in order for the application to be able to save the file
        correctParentPath = (parentPath.replace("\\", "/"))
        workbook = xlsxwriter.Workbook(correctParentPath + '/ExportedCSVFiles/'
                                       + moduleCodeSelection + "-" + assignmentSelect + '.xlsx')
        worksheet = workbook.add_worksheet()

        # Set the 'time_graded' column with the datetime for format
        format1 = workbook.add_format({'num_format': 'mmm d yyyy hh:mm:ss'})
        worksheet.set_column('C:C', 11)
        worksheet.set_column('D:D', 11)
        worksheet.set_column('F:F', 20, format1)
        worksheet.set_column('G:G', 51)

        try:
            # Writes the headings in the DB table into the xls file
            for column, heading in enumerate(cur.description):
                worksheet.write(0, column, heading[0])  # first element of each tuple

            # Writes the rows in the DB table into the xls file
            for rows, row in enumerate(assignmentData):
                for colindex, col in enumerate(row):
                    worksheet.write(rows + 1, colindex, col)
            workbook.close()

            print("File location of exported data: " + correctParentPath + '/ExportedCSVFiles/')

            exportDataConfirmed_lbl = tk.Label(window, text="Data Exported and saved", font=("Calibri", 12))
            exportDataConfirmed_lbl.place(x=550, y=125)

        except FileCreateError as error:
            print(str(error))
            exportDataConfirmed_lbl = tk.Label(window, text="Error saving file", fg="red", font=("Calibri", 12))
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
