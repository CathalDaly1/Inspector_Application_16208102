import smtplib
import tkinter as tk
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import count
from tkinter import ttk
from tkinter.ttk import Progressbar

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

    lbl_title = tk.Label(window, text="Inspector - Mailing System", font=("Arial Bold", 18))
    lbl_title.place(x=400, y=50, anchor="center")

    label_module = tk.Label(window, text="Choose module from list: ", font=("Calibri", 14))
    label_module.place(x=25, y=95)

    progress = Progressbar(window, orient=tk.HORIZONTAL,
                           length=100, mode='determinate')

    # As there are duplicates of assignments with module codes have to use distinct
    cur.execute("SELECT DISTINCT modulecode FROM assignments WHERE user_id =%s",
                (userID,))
    moduleCode = cur.fetchall()
    conn.commit()

    moduleCombobox = ttk.Combobox(window, values=moduleCode)
    moduleCombobox.place(x=230, y=100)

    def displayAssignment():
        """
        This docstring must be filled in
        """
        assignmentCombobox()

    def assignmentCombobox():
        """
        This docstring must be filled in
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
        bar()
        detailsSaved = tk.Label(window, text="Module code: " + str(moduleCodeSelection) + " and Assignment number: " +
                                             str(assignmentSelect),
                                font=("Calibri", 14))
        detailsSaved.place(x=25, y=180)
        global studentIdList
        numberOfRecipients = len(studentIdList)
        recipientsLoaded = tk.Label(window, text=str(numberOfRecipients) + " Recipient(s) loaded into email system",
                                    font=("Calibri", 14))
        recipientsLoaded.place(x=25, y=207)

    def bar():
        """
        This method displays a progress bar
        :rtype: object
        """
        import time
        progress['value'] = 20
        window.update_idletasks()
        time.sleep(0.45)

        progress['value'] = 40
        window.update_idletasks()
        time.sleep(0.45)

        progress['value'] = 50
        window.update_idletasks()
        time.sleep(0.45)

        progress['value'] = 60
        window.update_idletasks()
        time.sleep(0.45)

        progress['value'] = 80
        window.update_idletasks()
        time.sleep(0.45)
        progress['value'] = 100

    loading = tk.Label(window, text="Loading data into the email system: ", font=("Calibri", 14))
    loading.place(x=25, y=155)
    progress.place(x=273, y=157)

    def showTable():
        """
        This method works with list and tuple manipulation in python
        Firstly, select student ID numbers and associated filenames from the database
        concat the studentmail extension for each of the student numbers
        concat the pdf extension for each of the filenames
        Create a map converting student ids(ints) to strings. Also merge lists of the studeent IDs and filenames
        in order to get the file from the file system.
        """
        global moduleCodeSelection, assignmentSelect, studentEmail
        moduleCodeSelection = moduleCombobox.get()
        assignmentSelect = assignmentCombo.get()

        cur.execute("SELECT student_id from assignments where user_id=%s and modulecode=%s and assignmentno=%s",
                    (userID, moduleCodeSelection, assignmentSelect))
        studentID = cur.fetchall()

        global studentIdList
        studentIdList = [item for t in studentID for item in t]
        emailExtension = "@studentmail.ul.ie"

        global studentEmail, studentAssignment
        studentEmail = [str(s) + emailExtension for s in studentIdList]

        cur.execute("SELECT filename from assignments where user_id=%s and modulecode=%s and assignmentno=%s",
                    (userID, moduleCodeSelection, assignmentSelect))
        studentAssignment = cur.fetchall()

        filenameExt = [item for t in studentAssignment for item in t]
        fileExtension = ".pdf"
        global studentFilesWithExtension
        studentFilesWithExtension = [str(s) + fileExtension for s in filenameExt]

        # Convert list of ints to list of strings
        studentIDConvert = list(map(str, studentIdList))

        def mergeLists(list1, list2):
            merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
            return merged_list

        # Merging two lists in order to get filepath which gets the student ID and the name of the document
        filePathMergedList = mergeLists(studentIDConvert, studentFilesWithExtension)

        # Join the contents of the tuple and add a '/' for the filepath
        global filePathCreation
        filePathCreation = list(map('/'.join, filePathMergedList))

        displayModuleAssignments()

    def send_email():
        """
        This method will allow the user to send emails to students with attachment and grade.
        """
        try:
            global studentEmail, studentIdList, studentAssignment, studentFilesWithExtension
            # looping through the two lists using zip
            for f, a, c, m in zip(studentEmail, studentIdList, studentAssignment, studentFilesWithExtension):
                email_user = '16208102@studentmail.ul.ie'
                email_password = 'Detlef228425'
                email_send = f

                subject = emailSubjectEntry.get('1.0', 'end-1c')

                msg = MIMEMultipart()
                msg['From'] = email_user
                # msg['To'] = ",".join(email_send)
                msg['To'] = email_send
                msg['Subject'] = subject

                server = smtplib.SMTP('smtp-mail.outlook.com')
                server.starttls()
                server.login(email_user, email_password)

                filename = ("C:/Users/catha/OneDrive/Desktop/OneDrive/Assignments2/Graded Assignments/" + str(a)
                            + "/Corrected-" + str(m))

                # Attaching file to the email
                with open(filename, "rb") as attachment:
                    # Add file as application/octet-stream
                    # Email client can usually download this automatically as attachment
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                    encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )

                # get grade from database
                cur.execute(
                    "SELECT final_grade from assignments where user_id=%s and modulecode=%s and assignmentno=%s and student_id=%s and filename=%s",
                    (userID, moduleCodeSelection, assignmentSelect, a, c))
                studentFinalGrade = cur.fetchall()
                grade = [item for t in studentFinalGrade for item in t]
                body = emailBodyEntry.get('1.0', 'end-1c')
                body += "\n\n Final grade for this assignment = " + str(grade) + " Marks"
                msg.attach(MIMEText(body, 'plain'))
                msg.attach(part)

                text = msg.as_string()
                server.sendmail(email_user, email_send, text)
                server.quit()
                print("email has been sent to " + f)

                emailSent_lbl = tk.Label(window, text="Email Recipients: ", font=("Calibri", 14))
                emailSent_lbl.place(x=25, y=580)

                emailSentList: tk.Text = tk.Text(window, height="5", width="60")
                emailSentList.place(x=160, y=580)
                emailSentList.insert('1.0', "Email has been sent to:" + f)

        except Exception as error:
            print(str(error))
            print("Failed to send email")

    def back():
        """
        This method is called when the backbutton is pressed. Window is destroyed and closed.
        """
        window.destroy()

    saveModuleSelection = tk.Button(window, text="Display Assignments", fg="black", command=displayAssignment, width=15)
    saveModuleSelection.place(x=400, y=100)

    emailSubject_lbl = tk.Label(window, text="Email Subject: ", font=("Calibri", 14))
    emailSubject_lbl.place(x=25, y=255)

    emailSubjectEntry: tk.Text = tk.Text(window, height="2", width="60")
    emailSubjectEntry.place(x=160, y=260)

    emailBody_lbl = tk.Label(window, text="Email Body: ", font=("Calibri", 14))
    emailBody_lbl.place(x=25, y=320)

    emailBodyEntry: tk.Text = tk.Text(window, height="10", width="60")
    emailBodyEntry.place(x=160, y=325)

    sendEmailButton = tk.Button(window, text="Send emails", fg="black", command=send_email,
                                width=15)
    sendEmailButton.place(x=533, y=500)

    back_button = tk.Button(window, text="Back", fg="black", command=back, width=12)
    back_button.place(x=160, y=500)
