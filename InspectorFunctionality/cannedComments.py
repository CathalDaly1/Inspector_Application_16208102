import tkinter as tk

import InspectorFunctionality.loginUser
import InspectorFunctionality.connectToDB
import InspectorFunctionality.FileAccessScreen


def cannedCommentScreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("600x380+250+200")
    window.resizable(False, False)

    conn = InspectorFunctionality.connectToDB.connectToDB()
    cur = conn.cursor()

    moduleCode_lbl = tk.Label(window, fg="black", text="Module Code: ", font=("Calibri", 12))
    moduleCode_lbl.place(x=30, y=50)
    moduleCodeEntry: tk.Text = tk.Text(window, height="1", width="10")
    moduleCodeEntry.place(x=150, y=50)

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
        comment1 = commentsEntry1.get("1.0", 'end-1c')
        comment2 = commentsEntry2.get("1.0", 'end-1c')
        comment3 = commentsEntry3.get("1.0", 'end-1c')
        comment4 = commentsEntry4.get("1.0", 'end-1c')
        comment5 = commentsEntry5.get("1.0", 'end-1c')
        # When save button is pressed, save the comments and destroy the entry's and labels

        userID = InspectorFunctionality.loginUser.getUsername()
        cur.execute("SELECT * FROM cannedComments WHERE user_id=%s AND moduleCode = %s",
                    (userID, moduleCode))
        cannedComments = cur.fetchall()
        conn.commit()

        if not cannedComments:
            sql1 = "INSERT INTO cannedComments (user_id, moduleCode, comment1, comment2, comment3, comment4, comment5) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val1 = (userID, moduleCode, comment1, comment2, comment3, comment4, comment5)
            # Executes the insertion ans passes values username and password into the insertion
            cur.execute(sql1, val1)
            conn.commit()
            newCommentsSaved_lbl = tk.Label(window, text="Canned Comments have been saved", font=("Calibri", 10))
            newCommentsSaved_lbl.place(x=250, y=315)

        else:
            sql2 = "Update cannedComments set comment1 = %s, comment2 = %s , comment3 = %s , comment4 = %s , comment5 = %s where user_id =%s and moduleCode=%s"
            val2 = (comment1, comment2, comment3, comment4, comment5, userID, moduleCode)
            cur.execute(sql2, val2)
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
