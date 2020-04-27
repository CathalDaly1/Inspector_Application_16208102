import tkinter as tk

from DBConnection import connectToDB
import GradingFunctionality.AccessingFiles


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

    conn = connectToDB.connectToDatabase()
    cur = conn.cursor()

    moduleCode = GradingFunctionality.AccessingFiles.getModuleCode()
    assignmentNo = GradingFunctionality.AccessingFiles.getAssignmentNo()

    def saveAddedMarks():
        """This method adds a certain mark to all assignments in the database that have already been graded."""
        addedMarks = addMarksEntry.get("1.0", 'end-1c').upper()

        if addedMarks != "":
            cur.execute(
                "Update assignments set final_grade = final_grade + %s where modulecode =%s and assignmentNo = %s",
                (addedMarks, moduleCode, assignmentNo,))
            conn.commit()
            messageAddMarks = ("You have added: " + addedMarks + " marks to " + moduleCode
                               + " - Assignment No. " + assignmentNo + "\n")
            outputBox.insert(tk.END, messageAddMarks)
        else:
            messageSubMarks = "Please enter a value to add in the box above\n"
            outputBox.insert(tk.END, messageSubMarks)

    def saveSubtractedMarks():
        """ This method subtracts a certain mark to all assignments in the database that have already been graded."""
        subtractedMarks = addMarksEntry.get("1.0", 'end-1c').upper()
        if subtractedMarks != "":
            cur.execute(
                "Update assignments set final_grade = final_grade - %s where modulecode =%s and assignmentNo = %s",
                (subtractedMarks, moduleCode, assignmentNo,))
            conn.commit()
            messageSubMarks = ("You have subtracted: " + subtractedMarks + " marks from " + moduleCode
                               + " - Assignment No. " + assignmentNo + "\n")
            outputBox.insert(tk.END, messageSubMarks)
        else:
            messageSubMarks = "Please enter a value to subtract in the box above\n"
            outputBox.insert(tk.END, messageSubMarks)

    def closeWindow():
        """Closes window when button is pressed"""
        window.destroy()

    comments_lbl = tk.Label(window, fg="black", text="Add/Subtract marks from previously graded assignments",
                            font=("Calibri Bold", 14))
    comments_lbl.place(x=80, y=20)

    addMarks_lbl = tk.Label(window, fg="black", text="Enter number of marks you want to add/subtract: ",
                            font=("Calibri", 12))
    addMarks_lbl.place(x=50, y=80)
    addMarksEntry: tk.Text = tk.Text(window, height="1", width="10")
    addMarksEntry.place(x=380, y=82)

    addButton = tk.Button(window, text="Add", width=13, command=saveAddedMarks)
    addButton.place(x=50, y=120)

    subtractButton = tk.Button(window, text="Subtract", fg="red", width=13, command=saveSubtractedMarks)
    subtractButton.place(x=200, y=120)

    output_lbl = tk.Label(window, fg="black", text="Output: ", font=("Calibri", 12))
    output_lbl.place(x=50, y=170)
    outputBox = tk.Text(window, wrap=tk.NONE, height=6, width=65, borderwidth=0)
    outputBox.place(x=50, y=200)

    closeButton = tk.Button(window, text="Close", width=13, fg="red", command=closeWindow)
    closeButton.place(x=200, y=310)
