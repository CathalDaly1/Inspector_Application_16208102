import tkinter as tk

import DBConnection.connectToDB
from UserCredentials import loginUser
import GradingFunctionality.AccessingFiles


def menuOptions():
    """
    This method creates the tkinter window, labels and entry boxes in order for the user to enter comments and save
    them. Retrieves the key values, comments, canned comments and grading categories from the database for the
    associated modulecode and assignment number that was entered in the File Access Screen.
    :return:
    """
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("550x600+1250+50")
    window.resizable(False, False)
    window.attributes("-topmost", 1)

    conn = DBConnection.connectToDB.connectToDB()
    cur = conn.cursor()

    lbl_title = tk.Label(window, text="Inspector - Keystrokes", font=("Arial Bold", 18))
    lbl_title.pack()

    userID = loginUser.getUserID()
    assignmentModuleCode = GradingFunctionality.AccessingFiles.getModuleCode()
    assignmentNo = GradingFunctionality.AccessingFiles.getAssignmentNo()

    cur.execute(
        "SELECT comment1, comment2, comment3, comment4, comment5 FROM cannedComments WHERE user_id =%s and moduleCode = %s and assignmentNo = %s",
        (userID, assignmentModuleCode, assignmentNo))
    fetchedComments = cur.fetchone()

    try:
        comment1Display = fetchedComments[0]
        comment2Display = fetchedComments[1]
        comment3Display = fetchedComments[2]
        comment4Display = fetchedComments[3]
        comment5Display = fetchedComments[4]
    except TypeError:
        comment1Display = "You have not added Canned Comment 1"
        comment2Display = "You have not added Canned Comment 2"
        comment3Display = "You have not added Canned Comment 3"
        comment4Display = "You have not added Canned Comment 4"
        comment5Display = "You have not added Canned Comment 5"

    cur.execute(
        "SELECT  valueKeyA, commentA, valueKeyB, commentB,  valueKeyC, commentC, valueKeyD, commentD, total FROM keyscomments WHERE user_id =%s and modulecode = %s and assignmentno = %s",
        (userID, assignmentModuleCode, assignmentNo))
    fetchedKeyValuesDisplay = cur.fetchone()

    valueKeyADisplay = fetchedKeyValuesDisplay[0]
    commentADisplay = fetchedKeyValuesDisplay[1]
    valueKeyBDisplay = fetchedKeyValuesDisplay[2]
    commentBDisplay = fetchedKeyValuesDisplay[3]
    valueKeyCDisplay = fetchedKeyValuesDisplay[4]
    commentCDisplay = fetchedKeyValuesDisplay[5]
    valueKeyDDisplay = fetchedKeyValuesDisplay[6]
    commentDDisplay = fetchedKeyValuesDisplay[7]

    cur.execute(
        "SELECT  categoryA, categoryB, categoryC, categoryD,  categoryE  FROM gradingCategories WHERE user_id =%s and modulecode = %s and assignmentno = %s",
        (userID, assignmentModuleCode, assignmentNo))
    gradingCategories = cur.fetchone()

    try:
        gradingCategoriesA = gradingCategories[0]
        gradingCategoriesB = gradingCategories[1]
        gradingCategoriesC = gradingCategories[2]
        gradingCategoriesD = gradingCategories[3]
        gradingCategoriesE = gradingCategories[4]
    except TypeError:
        gradingCategoriesA = "You have not added Canned Comment 1"
        gradingCategoriesB = "You have not added Canned Comment 2"
        gradingCategoriesC = "You have not added Canned Comment 3"
        gradingCategoriesD = "You have not added Canned Comment 4"
        gradingCategoriesE = "You have not added Canned Comment 5"

    tk.Label(window, bg="white", justify=tk.LEFT,
             text="Key S: Start Grading" + "\n" + "Key A: +" + str(valueKeyADisplay) + " - Comment A: " + str(
                 commentADisplay) + "\n"
                                    "Key B: +" + str(
                 valueKeyBDisplay) + " - Comment B: " + str(commentBDisplay) + "\n"
                                                                               "Key C: +" + str(
                 valueKeyCDisplay) + " - Comment C: " + str(commentCDisplay) + "\n"
                                                                               "Key D: +" + str(
                 valueKeyDDisplay) + " - Comment D: " + str(commentDDisplay) + "\n"
                                                                               "Key E: Complete grading"
                  + "\n"
                    "Canned Comment 1: " + str(comment1Display)
                  + "\n"
                    "Canned Comment 2: " + str(comment2Display)
                  + "\n"
                    "Canned Comment 3: " + str(comment3Display)
                  + "\n"
                    "Canned Comment 4: " + str(comment4Display)
                  + "\n"
                    "Canned Comment 5: " + str(comment5Display)
                  + "\n"
                    "Category A: " + str(gradingCategoriesA)
                  + "\n"
                    "Category B: " + str(gradingCategoriesB)
                  + "\n"
                    "Category C: " + str(gradingCategoriesC)
                  + "\n"
                    "Category D: " + str(gradingCategoriesD)
                  + "\n"
                    "Category E: " + str(gradingCategoriesE), wraplengt=550, font=("Arial", 12)).pack()
