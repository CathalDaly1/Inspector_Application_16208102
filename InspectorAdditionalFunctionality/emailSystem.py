import smtplib
import tkinter as tk
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import ttk
import pandas as pd

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

    def assignmentCombobox():
        """
        This docsting must be filled in
        """
        global moduleCodeSelection, assignmentSelection, assignmentCombo
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

        saveAssignmentSelection = tk.Button(window, text="Save selection", fg="black", command=showTable, width=15)
        saveAssignmentSelection.place(x=400, y=127)

    def displayModuleAssignments():
        """
        This class retrieves assignment information from the assignments table in the database.
        """
        test = tk.Label(window, text="Module code: " + str(moduleCodeSelection) + " and Assignment number: " +
                                     str(assignmentSelect) + " saved", font=("Calibri", 14))
        test.place(x=25, y=160)

    def showTable():
        """
        This docsting must be filled in
        """
        global moduleCodeSelection, assignmentSelect
        moduleCodeSelection = moduleCombobox.get()
        assignmentSelect = assignmentCombo.get()
        displayModuleAssignments()

    # ToDo implement with tkinter and also implement attachments, not sure how I will do that
    def send_email():
        """
        This method will allow the user to send emails to students with attachment and grade.
        """
        try:
            email_user = '16208102@studentmail.ul.ie'
            email_password = ''
            email_send = ['cathald96@gmail.com', 'cathald96@gmail.com', 'cathald96@gmail.com']

            subject = emailSubjectEntry.get('1.0', 'end-1c')

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = ",".join(email_send)
            msg['Subject'] = subject

            server = smtplib.SMTP('smtp-mail.outlook.com')
            server.starttls()
            server.login(email_user, email_password)

            body = emailBodyEntry.get('1.0', 'end-1c')
            msg.attach(MIMEText(body, 'plain'))

            text = msg.as_string()
            server.sendmail(email_user, email_send, text)
            server.quit()
            print("email has been sent!")

        except Exception as error:
            print(str(error))
            print("Failed to send email")

    def back():
        """
        This docsting must be filled in
        """
        window.destroy()

    saveModuleSelection = tk.Button(window, text="Display Assignments", fg="black", command=displayAssignment, width=15)
    saveModuleSelection.place(x=400, y=100)

    emailSubject_lbl = tk.Label(window, text="Email Subject: ", font=("Calibri", 14))
    emailSubject_lbl.place(x=25, y=200)

    emailSubjectEntry: tk.Text = tk.Text(window, height="2", width="60")
    emailSubjectEntry.place(x=160, y=205)

    emailBody_lbl = tk.Label(window, text="Email Body: ", font=("Calibri", 14))
    emailBody_lbl.place(x=25, y=260)

    emailBodyEntry: tk.Text = tk.Text(window, height="10", width="60")
    emailBodyEntry.place(x=160, y=265)

    sendEmailButton = tk.Button(window, text="Send emails", fg="black", command=send_email,
                                width=15)
    sendEmailButton.place(x=400, y=600)

    back_button = tk.Button(window, text="Back", fg="black", command=back, height=2, width=12)
    back_button.place(x=350, y=730)
