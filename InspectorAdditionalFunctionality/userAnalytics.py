import tkinter as tk
import UserCredentials.loginUser
import DBConnection.connectToDB

from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

style.use('fivethirtyeight')

# ToDo Add new column in DB for module code and also assignment number or title

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()


def analyticsScreen():
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

    cols = ('Module Code', 'Student ID', 'Filename', 'Student Grade')
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
        assignmentCombobox()

    def refreshTable():
        listBox.delete(*listBox.get_children())

    def displayModuleAssignments():
        refreshTable()
        cur.execute("SELECT * FROM assignments WHERE user_id =%s and modulecode=%s",
                    (userID, moduleCodeSelection))

        assignmentData = cur.fetchall()
        conn.commit()

        for row in assignmentData:
            listBox.insert("", tk.END, values=(row[2], row[4], row[5], row[6]))

        assignmentID = []
        grade = []

        for row1 in assignmentData:
            assignmentID.append(row1[0])
            grade.append(row1[6])

            figure1 = Figure(figsize=(6, 4), dpi=80)
            subplot1 = figure1.add_subplot(111)
            xAxis = assignmentID
            yAxis = grade
            subplot1.bar(xAxis, yAxis, color='lightsteelblue')
            bar1 = FigureCanvasTkAgg(figure1, window)
            bar1.get_tk_widget().place(x=150, y=390)
            subplot1.set_title('Grade Distribution for ' + str(moduleCodeSelection))

    def assignmentCombobox():
        global moduleCodeSelection
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

    def showTable():
        global moduleCodeSelection
        moduleCodeSelection = moduleCombobox.get()
        displayModuleAssignments()

    def back():
        window.destroy()

    saveModuleSelection = tk.Button(window, text="Display Assignments", fg="black", command=displayAssignment, width=15)
    saveModuleSelection.place(x=400, y=100)

    back_button = tk.Button(window, text="Back", fg="black", command=back, height=2, width=12)
    back_button.place(x=350, y=730)