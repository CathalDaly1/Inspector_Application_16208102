import tkinter as tk

import DBConnection.connectToDB
import UserCredentials.loginUser
import InspectorGradingFunctionality.AccessingFiles


def menuOptions():
    """
    This method creates the tkinter window, labels and entry boxes in order for the user to enter
    comments and save them.
    :return:
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("600x520+1250+50")
    window.resizable(False, False)

    conn = DBConnection.connectToDB.connectToDB()
    cur = conn.cursor()

    lbl_title = tk.Label(window, text="Inspector - Keystrokes", font=("Arial Bold", 18))
    lbl_title.pack()

    userID = UserCredentials.loginUser.getUserID()
    assignmentModuleCode = InspectorGradingFunctionality.AccessingFiles.getModuleCode()
    assignmentNo = InspectorGradingFunctionality.AccessingFiles.getAssignmentNo()

    cur.execute(
        "SELECT  valueKeyA, commentA, valueKeyB, commentB,  valueKeyC, commentC, valueKeyD, commentD, total FROM keyscomments WHERE user_id =%s and modulecode = %s and assignmentno = %s",
        (userID, assignmentModuleCode, assignmentNo))
    fetchedKeyValuesDisplay = cur.fetchone()
    print("keys comments: " + str(fetchedKeyValuesDisplay))

    cur.execute(
        "SELECT comment1, comment2, comment3, comment4, comment5 FROM cannedComments WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
        (userID, assignmentModuleCode, assignmentNo))
    fetchedComments = cur.fetchone()
    print("Canned comments:" + str(fetchedComments))

    comment1Display = fetchedComments[0]
    comment2Display = fetchedComments[1]
    comment3Display = fetchedComments[2]
    comment4Display = fetchedComments[3]
    comment5Display = fetchedComments[4]

    valueKeyADisplay = fetchedKeyValuesDisplay[0]
    commentADisplay = fetchedKeyValuesDisplay[1]
    valueKeyBDisplay = fetchedKeyValuesDisplay[2]
    commentBDisplay = fetchedKeyValuesDisplay[3]
    valueKeyCDisplay = fetchedKeyValuesDisplay[4]
    commentCDisplay = fetchedKeyValuesDisplay[5]
    valueKeyDDisplay = fetchedKeyValuesDisplay[6]
    commentDDisplay = fetchedKeyValuesDisplay[7]

    tk.Label(window, bg="white", justify=tk.LEFT,
             text="Key S: Start Grading" + "\n" + "Key A: +" + str(valueKeyADisplay) + " - Comment A: " + str(
                 commentADisplay) + "\n\n"
                                    "Key B: +" + str(
                 valueKeyBDisplay) + " - Comment B: " + str(commentBDisplay) + "\n\n"
                                                                               "Key C: +" + str(
                 valueKeyCDisplay) + " - Comment C: " + str(commentCDisplay) + "\n\n"
                                                                               "Key D: +" + str(
                 valueKeyDDisplay) + " - Comment D: " + str(commentDDisplay) + "\n\n"
                                                                               "Key E: Exit grading"
                  + "\n\n"
                    "Canned Comment 1: " + str(comment1Display)
                  + "\n\n"
                    "Canned Comment 2: " + str(comment2Display)
                  + "\n\n"
                    "Canned Comment 3: " + str(comment3Display)
                  + "\n\n"
                    "Canned Comment 4: " + str(comment4Display)
                  + "\n\n"
                    "Canned Comment 5: " + str(comment5Display), wraplengt=550,
             font=("Arial", 12)).pack()
