import tkinter as tk

from DBConnection import connectToDB
from UserCredentials import loginUser
from GradingFunctionality import AccessingFiles


def cannedCommentScreen():
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

    userID = loginUser.getUserID()

    conn = connectToDB.connectToDatabase()
    cur = conn.cursor()

    comments_lbl = tk.Label(window, fg="black", text="Enter canned comments below",
                            font=("Calibri Bold", 16))
    comments_lbl.place(x=180, y=10)

    comment1_lbl = tk.Label(window, fg="black", text="Comment 1: ", font=("Calibri", 12))
    comment1_lbl.place(x=30, y=82)
    commentsEntry1: tk.Text = tk.Text(window, height="2", width="50")
    commentsEntry1.place(x=150, y=78)
    comment2_lbl = tk.Label(window, fg="black", text="Comment 2: ", font=("Calibri", 12))
    comment2_lbl.place(x=30, y=131)
    commentsEntry2: tk.Text = tk.Text(window, height="2", width="50")
    commentsEntry2.place(x=150, y=127)
    comment3_lbl = tk.Label(window, fg="black", text="Comment 3: ", font=("Calibri", 12))
    comment3_lbl.place(x=30, y=181)
    commentsEntry3: tk.Text = tk.Text(window, height="2", width="50")
    commentsEntry3.place(x=150, y=177)
    comment4_lbl = tk.Label(window, fg="black", text="Comment 4: ", font=("Calibri", 12))
    comment4_lbl.place(x=30, y=231)
    commentsEntry4: tk.Text = tk.Text(window, height="2", width="50")
    commentsEntry4.place(x=150, y=227)
    comment5_lbl = tk.Label(window, fg="black", text="Comment 5: ", font=("Calibri", 12))
    comment5_lbl.place(x=30, y=281)
    commentsEntry5: tk.Text = tk.Text(window, height="2", width="50")
    commentsEntry5.place(x=150, y=277)

    def displayPrevious():
        """
        This method allows the user to display previously saved canned comments of the associated module code and
        assignment No. Throw exception if the user clicks the edit button if there are no previous canned comments
        saved in the database.
        :rtype: object
        """
        moduleCode = AccessingFiles.getModuleCode()
        assignmentNo = AccessingFiles.getAssignmentNo()

        if moduleCode and assignmentNo != "":
            try:
                cur.execute("SELECT * FROM cannedComments WHERE user_id=%s AND moduleCode = %s AND assignmentno = %s",
                            (userID, moduleCode, assignmentNo))
                cannedComments = cur.fetchone()
                conn.commit()

                commentsEntry1.insert(tk.END, cannedComments[3])
                commentsEntry2.insert(tk.END, cannedComments[4])
                commentsEntry3.insert(tk.END, cannedComments[5])
                commentsEntry4.insert(tk.END, cannedComments[6])
                commentsEntry5.insert(tk.END, cannedComments[7])

            except TypeError:
                error_lbl = tk.Label(window, text="No Previous records saved in the database\t\t", fg="red",
                                     font=("Calibri", 10))
                error_lbl.place(x=200, y=315)
        else:
            error_lbl = tk.Label(window, text="Please enter Module Code and Assignment No.", fg="red",
                                 font=("Calibri", 10))
            error_lbl.place(x=200, y=315)

    def saveCommentsButton():
        """
        This method is called when the save button is pressed. The contents of each entry box are saved
        into the cannedComments table in the postgresql database table. If the module code entered has
        comments already associated with it in the database the comments will be updated, otherwise
        the comments will just be inserted into the database.
        :return: array of comments that have been saved
        """
        moduleCode = AccessingFiles.getModuleCode()
        assignmentNo = AccessingFiles.getAssignmentNo()

        if moduleCode or assignmentNo != "":
            cur.execute("SELECT * FROM cannedComments WHERE user_id=%s AND moduleCode = %s AND assignmentno = %s",
                        (userID, moduleCode, assignmentNo))
            cannedComments = cur.fetchall()
            conn.commit()

            comment1 = commentsEntry1.get("1.0", 'end-1c')
            comment2 = commentsEntry2.get("1.0", 'end-1c')
            comment3 = commentsEntry3.get("1.0", 'end-1c')
            comment4 = commentsEntry4.get("1.0", 'end-1c')
            comment5 = commentsEntry5.get("1.0", 'end-1c')
            # When save button is pressed, save the comments and destroy the entry's and labels

            if not cannedComments:
                insertComments = "INSERT INTO cannedComments (user_id, moduleCode, assignmentNo, comment1, comment2, comment3, comment4, comment5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val1 = (userID, moduleCode, assignmentNo, comment1, comment2, comment3, comment4, comment5)
                # Executes the insertion ans passes values username and password into the insertion
                cur.execute(insertComments, val1)
                conn.commit()
                newCommentsSaved_lbl = tk.Label(window, text="Canned Comments have been saved\t\t\t",
                                                font=("Calibri", 10))
                newCommentsSaved_lbl.place(x=200, y=315)

            else:
                updateComments = "Update cannedComments set comment1 = %s, comment2 = %s , comment3 = %s , comment4 = %s , comment5 = %s where user_id =%s and moduleCode=%s and assignmentNo = %s"
                val2 = (comment1, comment2, comment3, comment4, comment5, userID, moduleCode, assignmentNo)
                cur.execute(updateComments, val2)
                conn.commit()
                commentsUpdated_lbl = tk.Label(window, text="Canned Comments have been updated\t\t\t",
                                               font=("Calibri", 10))
                commentsUpdated_lbl.place(x=200, y=315)

            return [comment1, comment2, comment3, comment4, comment5]
        else:
            error_lbl = tk.Label(window, text="Please enter Module Code and Assignment No. in previous screen",
                                 fg="red",
                                 font=("Calibri", 10))
            error_lbl.place(x=180, y=315)

    def closeWindow():
        """
        This method is called when the close button is pressed and it destroys the tkinter canned comments window.
        """
        window.destroy()

    editButton = tk.Button(window, text="Edit Comments", width=13, command=displayPrevious)
    editButton.place(x=453, y=45)

    saveButton = tk.Button(window, text="Save", width=13, command=saveCommentsButton)
    saveButton.place(x=370, y=350)

    closeButton = tk.Button(window, text="Close", width=13, fg="red", command=closeWindow)
    closeButton.place(x=100, y=350)
