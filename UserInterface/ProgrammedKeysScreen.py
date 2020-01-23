import tkinter as tk


def programmedKeysWindow():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("400x400+300+300")

    # Add error handling to ensure data entered is only 1 letter: re.search(pattern, string var)
    def saveButton():
        key_A_lbl = tk.Label(window, fg="black", text="Key: A = " + key_A.get(), font=("Calibri", 12))
        key_A_lbl.place(x=250, y=150)
        key_B_lbl = tk.Label(window, fg="black", text="Key: B = " + key_B.get(), font=("Calibri", 12))
        key_B_lbl.place(x=250, y=200)
        key_C_lbl = tk.Label(window, fg="black", text="Key: C = " + key_C.get(), font=("Calibri", 12))
        key_C_lbl.place(x=250, y=250)
        key_D_lbl = tk.Label(window, fg="black", text="Key: D = " + key_D.get(), font=("Calibri", 12))
        key_D_lbl.place(x=250, y=300)
        print("Value for Key A = " + key_A.get())
        print("Value for Key B = " + key_B.get())
        print("Value for Key C = " + key_C.get())
        print("Value for Key D = " + key_D.get())

    def exitButton():
        print("Closing window")
        window.withdraw()

    lbl_title = tk.Label(window, text="Change value of keystrokes", font=("Arial Bold", 15))
    lbl_title.place(x=200, y=25, anchor="center")
    lbl_sub_title = tk.Label(window, text="Enter in the input fields below\n" + "the new values for the keystrokes\n",
                             font=("Arial", 15))
    lbl_sub_title.place(x=200, y=105, anchor="center")
    saveButton = tk.Button(window, text="Save", command=saveButton, height=1, width=6)
    saveButton.place(x=200, y=350)
    exit_button1 = tk.Button(window, text="Exit", command=exitButton, height=1, width=6)
    exit_button1.place(x=100, y=350)

    # KeyStroke A
    text_A_lbl = tk.Label(window, fg="black", text="Enter New Value for A: ", font=("Calibri", 12))
    text_A_lbl.place(x=0, y=150)
    key_A = tk.Entry(window, width="10")
    key_A.place(x=160, y=150)
    key_A.insert(0, "")

    # KeyStroke B
    text_B_lbl = tk.Label(window, fg="black", text="Enter New Value for B: ", font=("Calibri", 12))
    text_B_lbl.place(x=0, y=200)
    key_B = tk.Entry(window, width="10")
    key_B.place(x=160, y=200)
    key_B.insert(0, "")

    # KeyStroke C
    text_C_lbl = tk.Label(window, fg="black", text="Enter New Value for C: ", font=("Calibri", 12))
    text_C_lbl.place(x=0, y=250)
    key_C = tk.Entry(window, width="10")
    key_C.place(x=160, y=250)
    key_C.insert(0, "")

    # KeyStroke D
    text_D_lbl = tk.Label(window, fg="black", text="Enter New Value for D: ", font=("Calibri", 12))
    text_D_lbl.place(x=0, y=300)
    key_D = tk.Entry(window, width="10")
    key_D.place(x=160, y=300)
    key_D.insert(0, "")

