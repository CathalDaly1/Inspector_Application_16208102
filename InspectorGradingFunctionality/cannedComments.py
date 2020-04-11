import tkinter as tk

import UserCredentials.loginUser
import DBConnection.connectToDB


def cannedCommentScreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("600x380+250+200")
    window.resizable(False, False)

    conn = DBConnection.connectToDB.connectToDB()
    cur = conn.cursor()

    moduleCode_lbl = tk.Label(window, fg="black", text="Module Code: ", font=("Calibri", 12))
    moduleCode_lbl.place(x=30, y=50)
    moduleCodeEntry: tk.Text = tk.Text(window, height="1", width="10")
    moduleCodeEntry.place(x=150, y=50)

    assignmentNo_lbl = tk.Label(window, fg="black", text="Assignment No.: ", font=("Calibri", 12))
    assignmentNo_lbl.place(x=230, y=50)
    assignmentNoEntry: tk.Text = tk.Text(window, height="1", width="10")
    assignmentNoEntry.place(x=350, y=50)

    comments_lbl = tk.Label(window, fg="black", text="Enter canned comments below",
                            font=("Calibri Bold", 14))
    comments_lbl.place(x=200, y=20)
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

    def saveCommentsButton():
        moduleCode = moduleCodeEntry.get("1.0", 'end-1c')
        assignmentNo = assignmentNoEntry.get("1.0", 'end-1c')
        comment1 = commentsEntry1.get("1.0", 'end-1c')
        comment2 = commentsEntry2.get("1.0", 'end-1c')
        comment3 = commentsEntry3.get("1.0", 'end-1c')
        comment4 = commentsEntry4.get("1.0", 'end-1c')
        comment5 = commentsEntry5.get("1.0", 'end-1c')
        # When save button is pressed, save the comments and destroy the entry's and labels

        userID = UserCredentials.loginUser.getUserID()
        cur.execute("SELECT * FROM cannedComments WHERE user_id=%s AND moduleCode = %s AND assignmentno = %s",
                    (userID, moduleCode, assignmentNo))
        cannedComments = cur.fetchall()
        conn.commit()

        if not cannedComments:
            insertComments = "INSERT INTO cannedComments (user_id, moduleCode, assignmentNo, comment1, comment2, comment3, comment4, comment5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val1 = (userID, moduleCode, assignmentNo, comment1, comment2, comment3, comment4, comment5)
            # Executes the insertion ans passes values username and password into the insertion
            cur.execute(insertComments, val1)
            conn.commit()
            newCommentsSaved_lbl = tk.Label(window, text="Canned Comments have been saved", font=("Calibri", 10))
            newCommentsSaved_lbl.place(x=250, y=315)

        else:
            updateComments = "Update cannedComments set comment1 = %s, comment2 = %s , comment3 = %s , comment4 = %s , comment5 = %s where user_id =%s and moduleCode=%s and assignmentNo = %s"
            val2 = (comment1, comment2, comment3, comment4, comment5, userID, moduleCode, assignmentNo)
            cur.execute(updateComments, val2)
            conn.commit()
            commentsUpdated_lbl = tk.Label(window, text="Canned Comments have been updated", font=("Calibri", 10))
            commentsUpdated_lbl.place(x=250, y=315)

        return [comment1, comment2, comment3, comment4, comment5]

    def closeWindow():
        window.destroy()

    saveButton = tk.Button(window, text="Save", width=13, command=saveCommentsButton)
    saveButton.place(x=370, y=350)

    closeButton = tk.Button(window, text="Close", width=13, fg="red", command=closeWindow)
    closeButton.place(x=100, y=350)
