import datetime
import os
import random
import tkinter as tk
from tkinter import ttk

import matplotlib
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from pandas import DataFrame

import UserInterface.loginUser

import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

style.use('fivethirtyeight')


def connectToDB():
    connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Cannot connect to the DB")


conn = connectToDB()
cur = conn.cursor()


def analyticsScreen():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("850x800+100+100")
    window.resizable(False, False)

    userID = UserInterface.loginUser.getUsername()
    cur.execute("SELECT count(*) FROM assignments WHERE user_id =%s",
                (userID,))
    number = cur.fetchone()
    num = int(number[0])

    lbl_title = tk.Label(window, text="Inspector - Grading Analysis", font=("Arial Bold", 18))
    lbl_title.place(x=400, y=70, anchor="center")

    numberOfAssignmentsGraded_lbl = tk.Label(window, fg="black", text="Number of Assignments graded: " + str(num),
                                             font=("Calibri", 14))
    numberOfAssignmentsGraded_lbl.place(x=25, y=125)

    cols = ('Student ID', 'Filename', 'Student Grade', 'Graded - Timestamp')
    listBox = ttk.Treeview(window, columns=cols, show='headings')

    # Added scrollbar onto the listbox
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=listBox.yview)
    listBox['yscroll'] = scrollbar.set

    scrollbar.place(in_=listBox, relx=1.0, relheight=1.0, bordermode="outside")

    for col in cols:
        listBox.heading(col, text=col)
        listBox.place(x=25, y=160)

    cur.execute("SELECT * FROM assignments WHERE user_id =%s",
                (userID,))
    rows = cur.fetchall()
    for row in rows:
        listBox.insert("", tk.END, values=(row[2], row[3], row[4], row[6]))

    def graph_data():
        assignmentID = []
        grade = []

        for row1 in rows:
            assignmentID.append(row1[0])
            grade.append(row1[4])

            figure1 = Figure(figsize=(6, 4), dpi=80)
            subplot1 = figure1.add_subplot(111)
            xAxis = assignmentID
            yAxis = grade
            subplot1.bar(xAxis, yAxis, color='lightsteelblue')
            bar1 = FigureCanvasTkAgg(figure1, window)
            bar1.get_tk_widget().place(x=150, y=390)
            subplot1.set_title('Grade Distribution')

    graph_data()

    def back():
        window.destroy()

    back_button = tk.Button(window, text="Back", fg="black", command=back, height=2, width=12)
    back_button.place(x=350, y=730)
