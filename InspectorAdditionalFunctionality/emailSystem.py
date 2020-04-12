import tkinter as tk
from tkinter import ttk

import DBConnection.connectToDB
import UserCredentials.loginUser

conn = DBConnection.connectToDB.connectToDB()
cur = conn.cursor()


def emailSystem():
    """
    This class creates a tkinter window which will allow the user to send mass emails to students with assignments
    attached.
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("850x800+100+100")
    window.resizable(False, False)

    userID = UserCredentials.loginUser.getUserID()

    lbl_title = tk.Label(window, text="Inspector - Email System", font=("Arial Bold", 18))
    lbl_title.place(x=400, y=50, anchor="center")

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
        This docsting must be filled in
        """
        assignmentCombobox()

    def displayModuleAssignments():
        """
        This class retrieves assignment information from the assignments table in the database.
        """
        cur.execute("SELECT * FROM assignments WHERE user_id =%s and modulecode=%s",
                    (userID, moduleCodeSelection))

        assignmentData = cur.fetchall()
        print(assignmentData)
        conn.commit()

    def assignmentCombobox():
        """
        This docsting must be filled in
        """
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
        """
        This docsting must be filled in
        """
        global moduleCodeSelection
        moduleCodeSelection = moduleCombobox.get()
        displayModuleAssignments()

    def back():
        """
        This docsting must be filled in
        """
        window.destroy()

    saveModuleSelection = tk.Button(window, text="Display Assignments", fg="black", command=displayAssignment, width=15)
    saveModuleSelection.place(x=400, y=100)

    back_button = tk.Button(window, text="Back", fg="black", command=back, height=2, width=12)
    back_button.place(x=350, y=730)
