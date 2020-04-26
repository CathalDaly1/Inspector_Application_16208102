import tkinter as tk

import DBConnection.connectToDB
from UserCredentials import loginUser
import GradingFunctionality.AccessingFiles


def gradingCategoriesScreen():
    """
    This method creates the tkinter window, labels and entry boxes in order for the user to enter
    comments and save them.
    :rtype: object
    :return:
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("600x380+250+200")
    window.resizable(False, False)
    window.attributes("-topmost", 1)

    userID = loginUser.getUserID()

    conn = DBConnection.connectToDB.connectToDB()
    cur = conn.cursor()

    categories_lbl = tk.Label(window, fg="black", text="Enter Grading Categories below",
                              font=("Calibri Bold", 16))
    categories_lbl.place(x=180, y=10)

    categoriesA_lbl = tk.Label(window, fg="black", text="Category A: ", font=("Calibri", 12))
    categoriesA_lbl.place(x=30, y=82)
    categoriesEntryA: tk.Text = tk.Text(window, height="2", width="50")
    categoriesEntryA.place(x=150, y=78)
    categoriesB_lbl = tk.Label(window, fg="black", text="Category B ", font=("Calibri", 12))
    categoriesB_lbl.place(x=30, y=131)
    categoriesEntryB: tk.Text = tk.Text(window, height="2", width="50")
    categoriesEntryB.place(x=150, y=127)
    categoriesC_lbl = tk.Label(window, fg="black", text="Category C: ", font=("Calibri", 12))
    categoriesC_lbl.place(x=30, y=181)
    categoriesEntryC: tk.Text = tk.Text(window, height="2", width="50")
    categoriesEntryC.place(x=150, y=177)
    categoriesD_lbl = tk.Label(window, fg="black", text="Category D: ", font=("Calibri", 12))
    categoriesD_lbl.place(x=30, y=231)
    categoriesEntryD: tk.Text = tk.Text(window, height="2", width="50")
    categoriesEntryD.place(x=150, y=227)
    categoriesE_lbl = tk.Label(window, fg="black", text="Category E: ", font=("Calibri", 12))
    categoriesE_lbl.place(x=30, y=281)
    categoriesEntryE: tk.Text = tk.Text(window, height="2", width="50")
    categoriesEntryE.place(x=150, y=277)

    def displayPreviousCategories():
        """
        This method allows the user to display previously saved grading categories of the associated module code and
        assignment No. Throw exception if the user clicks the edit button if there are no previous grading categories
        saved in the database.
        :rtype: object
        """
        moduleCode = GradingFunctionality.AccessingFiles.getModuleCode()
        assignmentNo = GradingFunctionality.AccessingFiles.getAssignmentNo()

        if moduleCode and assignmentNo != "":
            try:
                cur.execute(
                    "SELECT * FROM gradingCategories WHERE user_id=%s AND moduleCode = %s AND assignmentno = %s",
                    (userID, moduleCode, assignmentNo))
                categories = cur.fetchone()
                conn.commit()

                categoriesEntryA.insert(tk.END, categories[3])
                categoriesEntryB.insert(tk.END, categories[4])
                categoriesEntryC.insert(tk.END, categories[5])
                categoriesEntryD.insert(tk.END, categories[6])
                categoriesEntryE.insert(tk.END, categories[7])

            except TypeError:
                error_lbl = tk.Label(window, text="No Previous records saved in the database\t\t", fg="red",
                                     font=("Calibri", 10))
                error_lbl.place(x=200, y=315)
        else:
            error_lbl = tk.Label(window, text="Please enter Module Code and Assignment No.", fg="red",
                                 font=("Calibri", 10))
            error_lbl.place(x=200, y=315)

    def saveCategoriesButton():
        """
        This method is called when the save button is pressed. The contents of each entry box are saved
        into the cannedComments table in the postgresql database table. If the module code entered has
        comments already associated with it in the database the comments will be updated, otherwise
        the comments will just be inserted into the database.
        :return:
        """
        moduleCode = GradingFunctionality.AccessingFiles.getModuleCode()
        assignmentNo = GradingFunctionality.AccessingFiles.getAssignmentNo()

        if moduleCode or assignmentNo != "":
            cur.execute("SELECT * FROM gradingCategories WHERE user_id=%s AND moduleCode = %s AND assignmentno = %s",
                        (userID, moduleCode, assignmentNo))
            gradingCategory = cur.fetchall()
            conn.commit()

            categoryA = categoriesEntryA.get("1.0", 'end-1c')
            categoryB = categoriesEntryB.get("1.0", 'end-1c')
            categoryC = categoriesEntryC.get("1.0", 'end-1c')
            categoryD = categoriesEntryD.get("1.0", 'end-1c')
            categoryE = categoriesEntryE.get("1.0", 'end-1c')

            if not gradingCategory:
                insertCategories = "INSERT INTO gradingCategories (user_id, moduleCode, assignmentNo, categoryA, categoryB, categoryC, categoryD, categoryE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val1 = (userID, moduleCode, assignmentNo, categoryA, categoryB, categoryC, categoryD, categoryE)
                # Executes the insertion ans passes values username and password into the insertion
                cur.execute(insertCategories, val1)
                conn.commit()
                newCommentsSaved_lbl = tk.Label(window, text="Grading Categories have been saved",
                                                font=("Calibri", 10))
                newCommentsSaved_lbl.place(x=230, y=315)

            else:
                updateCategories = "Update gradingCategories set categoryA = %s, categoryB = %s , categoryC = %s , categoryD = %s , categoryE = %s where user_id =%s and moduleCode=%s and assignmentNo = %s"
                val2 = (categoryA, categoryB, categoryC, categoryD, categoryE, userID, moduleCode, assignmentNo)
                cur.execute(updateCategories, val2)
                conn.commit()
                commentsUpdated_lbl = tk.Label(window, text="Grading Categories have been updated",
                                               font=("Calibri", 10))
                commentsUpdated_lbl.place(x=250, y=315)

            return [categoryA, categoryB, categoryC, categoryD, categoryE]
        else:
            error_lbl = tk.Label(window, text="Please enter Module Code and Assignment No.", fg="red",
                                 font=("Calibri", 10))
            error_lbl.place(x=200, y=315)

    def closeWindow():
        """
        This method is called when the close button is pressed and it destroys the tkinter canned comments window.
        """
        window.destroy()

    editButton = tk.Button(window, text="Edit Categories", width=13, command=displayPreviousCategories)
    editButton.place(x=453, y=45)

    saveButton = tk.Button(window, text="Save", width=13, command=saveCategoriesButton)
    saveButton.place(x=370, y=350)

    closeButton = tk.Button(window, text="Close", width=13, fg="red", command=closeWindow)
    closeButton.place(x=100, y=350)
