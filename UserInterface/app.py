import os
import tkinter as tk
import tkinter.ttk as ttk


def fileAccess():
    window = tk.Tk()
    window.title("Inspector - Grading Application")
    window.geometry("950x950+50+50")
    window.resizable(False, False)
    tree = ttk.Treeview(window)
    ysb = ttk.Scrollbar(window, orient='vertical', command=tree.yview)
    xsb = ttk.Scrollbar(window, orient='horizontal', command=tree.xview)
    tree.configure(yscroll=ysb.set, xscroll=xsb.set)

    abspath = os.path.abspath(path)
    root_node = tree.insert('', 'end', text=abspath, open=True)
    process_directory(root_node, abspath)

    tree.grid(row=0, column=0)
    ysb.grid(row=0, column=1, sticky='ns')
    xsb.grid(row=1, column=0, sticky='ew')
    window.grid()


def process_directory(window, parent, path):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        isdir = os.path.isdir(abspath)
        oid = window.tree.insert(parent, 'end', text=p, open=False)
        if isdir:
            window.process_directory(oid, abspath)


path_to_my_project = 'C:/Users/catha/OneDrive - University of Limerick/test2'
path = path_to_my_project
