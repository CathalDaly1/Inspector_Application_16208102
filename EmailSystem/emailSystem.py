import os
import smtplib
import tkinter as tk
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import ttk
from tkinter.ttk import Progressbar
from gevent._compat import izip

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

    def assignmentCombobox():
        """
        Get the information for the "Assignment No." dropdown list
        Retrieves the assignment numbers that are in the database for the user that is logged in
        and for the module code that they have entered in the module code dropdown list.
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
        This method retrieves the selections from the module code and assignment No. dropdown lists.
        This information is displayed on the GUI screen.
        """
        bar()
        global assignmentSelect, studentIdList
        detailsSaved = tk.Label(window, text="Module code: " + str(moduleCodeSelection) + " and Assignment number: " +
                                             str(assignmentSelect),
                                font=("Calibri", 14))
        detailsSaved.place(x=25, y=180)

        numberOfRecipients = len(studentIdList)

        recipientsLoaded = tk.Label(window, text=str(numberOfRecipients) + " Recipient(s) loaded into email system",
                                    font=("Calibri", 14))
        recipientsLoaded.place(x=25, y=207)

        studentGradeMessage_lbl = tk.Label(window, text="Students graded assignment and grade will be "
                                                        "automatically included in the email",
                                           font=("Calibri", 14))
        studentGradeMessage_lbl.place(x=25, y=233)

    def bar():
        """
        This method displays a progress bar which increases every 0.45 seconds.
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
    progress.place(x=305, y=158)

    def showTable():
        """
        This method retrieves the student ID numbers from the database for the assignment No and module code
        that was selected in the dropdown lists. Converts the list of tuples into a list of student ID's
        """
        global assignmentSelect, studentIdList
        assignmentSelect = assignmentCombo.get()

        cur.execute("SELECT DISTINCT student_id from assignments where user_id=%s and modulecode=%s and assignmentno=%s",
                    (userID, moduleCodeSelection, assignmentSelect))
        studentID = cur.fetchall()

        studentIdList = [item for t in studentID for item in t]

        displayModuleAssignments()

    def convertListToString(s):
        """This method converts a list into a string.
        :param s:
        :return:
        """
        # initialize an empty string
        conversionString = ""

        # traverse in the string
        for element in s:
            conversionString += element

        # return string
        return conversionString

    def send_email():
        """
        This method will allow the user to send emails to students with attachment and grade.
        Student ID numbers and associated filenames from the database concat the studentmail
        extension for each of the student numbers concat the pdf extension for each of the filenames.
        Throw an exception if the application is unable to connect to the mail server.
        :rtype: object
        """
        emailExtension = "@studentmail.ul.ie"

        studentEmail = [str(s) + emailExtension for s in studentIdList]

        cur.execute("SELECT filename from assignments where user_id=%s and modulecode=%s and assignmentno=%s",
                    (userID, moduleCodeSelection, assignmentSelect))
        studentAssignment = cur.fetchall()

        filenameExt = [item for t in studentAssignment for item in t]
        fileExtension = ".pdf"

        studentFilesWithExtension = [str(s) + fileExtension for s in filenameExt]

        try:
            # looping through several lists using zip
            for f, a, c, m in zip(studentEmail, studentIdList, studentAssignment, studentFilesWithExtension):
                # The email and password may be from an admin email account
                email_user = '16208102@studentmail.ul.ie'
                email_password = 'Detlef228425'
                email_send = f

                subject = emailSubjectEntry.get('1.0', 'end-1c')

                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = email_send
                msg['Subject'] = subject

                # Create SMTP outlook server which will be used to send email to studentmail.ul.ie accounts
                server = smtplib.SMTP('smtp-mail.outlook.com')
                server.starttls()
                server.login(email_user, email_password)

                cur.execute(
                    "SELECT DISTINCT filepath from assignments where user_id=%s and modulecode=%s and assignmentno=%s and student_id=%s and filename=%s",
                    (userID, moduleCodeSelection, assignmentSelect, a, c))
                fetchedFilepath = cur.fetchone()

                extractFilepath = (convertListToString(fetchedFilepath))
                correctPath = (extractFilepath.replace("\\", "/"))

                # Attaching file to the email
                listOfFiles = os.listdir(str(correctPath) + "/Graded Assignments/" + str(a))
                filePathString = (str(correctPath) + "/Graded Assignments/" + str(a) + "/")
                concatPathAndFiles = [filePathString + s for s in listOfFiles]

                # Loop through the files in each folder and attach the graded assignment(s) to the email for each student
                for files in concatPathAndFiles:
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(files, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(files)))
                    msg.attach(part)

                # Retrieve the students final grade from database
                cur.execute(
                    "SELECT final_grade from assignments where user_id=%s and modulecode=%s and assignmentno=%s and student_id=%s",
                    (userID, moduleCodeSelection, assignmentSelect, a))
                studentFinalGrade = cur.fetchall()

                # Fetch grades from database, sum the tuples if there are more than one grade for one student
                sumOfGrades = [sum(x) for x in izip(*studentFinalGrade)]

                body = emailBodyEntry.get('1.0', 'end-1c')
                body += "\n\n Final grade for this assignment = " + str(sumOfGrades) + " Marks"
                msg.attach(MIMEText(body, 'plain'))

                text = msg.as_string()
                server.sendmail(email_user, email_send, text)
                server.quit()
                print("email has been sent to " + f)

                emailSent_lbl = tk.Label(window, text="Email Recipients: ", font=("Calibri", 14))
                emailSent_lbl.place(x=25, y=580)

                emailSentList: tk.Text = tk.Text(window, height="5", width="60")
                emailSentList.place(x=160, y=580)
                emailSentList.insert('1.0', "Email has been sent to:" + f)

        # Throw exception: if connection to mail server was unsuccessful
        except Exception as error:
            print(str(error))
            print("Failed to send email")

    def back():
        """This method is called when the backbutton is pressed. Window is destroyed and closed."""
        window.destroy()

    saveModuleSelection = tk.Button(window, text="Display Assignments", fg="black", command=assignmentCombobox, width=15)
    saveModuleSelection.place(x=400, y=100)

    emailSubject_lbl = tk.Label(window, text="Email Subject: ", font=("Calibri", 14))
    emailSubject_lbl.place(x=25, y=260)

    emailSubjectEntry: tk.Text = tk.Text(window, height="2", width="60")
    emailSubjectEntry.place(x=160, y=265)

    emailBody_lbl = tk.Label(window, text="Email Body: ", font=("Calibri", 14))
    emailBody_lbl.place(x=25, y=320)

    emailBodyEntry: tk.Text = tk.Text(window, height="10", width="60")
    emailBodyEntry.place(x=160, y=325)

    sendEmailButton = tk.Button(window, text="Send emails", fg="black", command=send_email,
                                width=15)
    sendEmailButton.place(x=533, y=500)

    back_button = tk.Button(window, text="Back", fg="black", command=back, width=12)
    back_button.place(x=160, y=500)
