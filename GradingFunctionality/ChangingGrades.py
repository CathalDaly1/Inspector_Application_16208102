import tkinter as tk

import DBConnection.connectToDB


def changeStudentsGrades():
    """
    This method creates the tkinter window, labels and entry boxes in order for the user to enter
    comments and save them.
    :return:
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("600x380+250+200")
    window.resizable(False, False)
    window.attributes("-topmost", 1)

    conn = DBConnection.connectToDB.connectToDB()
    cur = conn.cursor()

    moduleCode_lbl = tk.Label(window, fg="black", text="Module Code: ", font=("Calibri", 12))
    moduleCode_lbl.place(x=50, y=50)
    moduleCodeEntry: tk.Text = tk.Text(window, height="1", width="10")
    moduleCodeEntry.place(x=150, y=53)

    assignmentNo_lbl = tk.Label(window, fg="black", text="Assignment No.: ", font=("Calibri", 12))
    assignmentNo_lbl.place(x=230, y=50)
    assignmentNoEntry: tk.Text = tk.Text(window, height="1", width="10")
    assignmentNoEntry.place(x=350, y=53)

    addMarks_lbl = tk.Label(window, fg="black", text="Enter number of marks you want to add/subtract: ",
                            font=("Calibri", 12))
    addMarks_lbl.place(x=50, y=140)
    addMarksEntry: tk.Text = tk.Text(window, height="1", width="10")
    addMarksEntry.place(x=380, y=142)

    output_lbl = tk.Label(window, fg="black", text="Output: ", font=("Calibri", 12))
    output_lbl.place(x=50, y=245)
    outputBox = tk.Text(window, wrap=tk.NONE, height=6, width=65, borderwidth=0)
    outputBox.place(x=50, y=270)

    def saveAddedMarks():
        """
        This method adds a certain mark to all assignments in the database that have already been graded
        """
        addedMarks = addMarksEntry.get("1.0", 'end-1c').upper()
        moduleCode = moduleCodeEntry.get("1.0", 'end-1c').upper()
        assignmentNo = assignmentNoEntry.get("1.0", 'end-1c').upper()

        cur.execute(
            "Update assignments set final_grade = final_grade + %s where modulecode =%s and assignmentNo = %s",
            (addedMarks, moduleCode, assignmentNo,))
        conn.commit()
        messageAddMarks = ("You have added: " + addedMarks + " marks from " + moduleCode
                   + " - Assignment No. " + assignmentNo + "\n")
        outputBox.insert(tk.END, messageAddMarks)

    def saveSubtractedMarks():
        """ This method subtracts a certain mark to all assignments in the database that have already been graded """
        subtractedMarks = addMarksEntry.get("1.0", 'end-1c').upper()
        moduleCode = moduleCodeEntry.get("1.0", 'end-1c').upper()
        assignmentNo = assignmentNoEntry.get("1.0", 'end-1c').upper()
        cur.execute(
            "Update assignments set final_grade = final_grade - %s where modulecode =%s and assignmentNo = %s",
            (subtractedMarks, moduleCode, assignmentNo,))
        conn.commit()
        messageSubMarks = ("You have subtracted: " + subtractedMarks + " marks from " + moduleCode
                           + " - Assignment No. " + assignmentNo + "\n")
        outputBox.insert(tk.END, messageSubMarks)

    comments_lbl = tk.Label(window, fg="black", text="Select button below to Add/Subtract marks",
                            font=("Calibri Bold", 14))
    comments_lbl.place(x=50, y=20)

    addButton = tk.Button(window, text="Add", width=13, command=saveAddedMarks)
    addButton.place(x=50, y=200)

    subtractButton = tk.Button(window, text="Subtract", fg="red", width=13, command=saveSubtractedMarks)
    subtractButton.place(x=200, y=200)
