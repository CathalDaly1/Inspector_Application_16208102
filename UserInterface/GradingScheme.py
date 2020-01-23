import tkinter as tk


def gradingSchemeWindow():
    print("Change grading scheme button clicked")
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("400x400+300+300")

    def saveButtonGrading():
        newGrade = tk.Label(window, fg="black", text="New grading scheme total = " + gradingSchemeTotal.get() + " marks", font=("Calibri", 12))
        newGrade.place(x=130, y=200, anchor="center")

    def exitButtonGrading():
        print("Closing window")
        window.withdraw()

    lbl_title_grading = tk.Label(window, text="Change grading scheme", font=("Arial Bold", 15))
    lbl_title_grading.place(x=200, y=25, anchor="center")
    lbl_sub_title_grading = tk.Label(window, text="Enter  below the total \n" + "marks for the class assignment\n",
                                     font=("Arial", 15))
    lbl_sub_title_grading.place(x=200, y=105, anchor="center")
    saveButton = tk.Button(window, text="Save", command=saveButtonGrading, height=1, width=6)
    saveButton.place(x=200, y=350)
    exit_button1 = tk.Button(window, text="Exit", command=exitButtonGrading, height=1, width=6)
    exit_button1.place(x=100, y=350)

    # Total amount of marks
    text_A_lbl = tk.Label(window, fg="black", text="Enter total amount of marks ", font=("Calibri", 12))
    text_A_lbl.place(x=0, y=150)
    gradingSchemeTotal = tk.Entry(window, width="10")
    gradingSchemeTotal.place(x=220, y=150)
    gradingSchemeTotal.insert(0, "")