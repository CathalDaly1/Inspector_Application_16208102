import tkinter as tk


def displayFileContents():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("800x800+100+100")

    def back():
        window.withdraw()

    studentID = "Implement"

    lbl_title = tk.Label(window, text="Assignment correction", font=("Arial Bold", 20))
    lbl_title.place(x=400, y=25, anchor="center")

    lbl_sub_title = tk.Label(window, text="Student: //" + studentID + "'s program", font=("Arial", 15))
    lbl_sub_title.place(x=400, y=200, anchor="center")

    # ToDo Get the name and student ID number of the student and display on this screen
    # ToDo Add keylogger in python in order to keep track of the totalling keys pressed in application
    # ToDo Display what keys have been pressed and there must be a way that the lecturer can remove choices if mistake has been made
    # ToDo Create a small table which will display logs and also display total amount of marks - LIVE

    T = tk.Text(window, state="normal", height=20, width=80)
    T.place(x=70, y=250)

    backButton = tk.Button(window, text="Back", width=15, command=back)
    backButton.place(x=150, y=600)

    file = 'C:/Users/catha/OneDrive - University of Limerick/test2/test111.py'
    T.insert(tk.END, open(file).read())


    # x = filedialog.askopenfilename()
    # print(x)
    #
    # T = tk.Text(window, state="normal", height=15, width=60)
    # T.pack()
    # T.insert(tk.END, open(x).read())
    # b = T.get("1.0", tk.END)
    #
    # f = open(x, 'wt')
    # f.write(b)
    # f.close()

# openButton1 = tk.Button(window, text="open now", command=DisplayStudentProgram.displayFileContents, height=1, width=6)
# openButton1.place(x=500, y=50)

# window = tk.Tk()
# window.fileName = filedialog.askopenfilename(filetypes=(("Python Stuff", ".py"), ("All files", "*,*")))
# print(window.fileName)
#
# text1 = open(window.fileName).read()
# print(text1)
#
# T = tk.Text(window, height=15, width=95)
# T.place(x=10, y=200)
#
# T.insert(tk.END, text1)
#
# b = T.get("1.0", tk.END)
# print(b)
#
# f = open(text1, 'wt')
# f.write(b)
# f.close()
