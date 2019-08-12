# import CSV Files from IDPS
from tkinter import *
from tkinter import filedialog
import csv


def choose_file():
    project = Tk()
    project.filename = filedialog.askopenfilename(initialdir="/", title="Choose an IDPS CSV file",
                                                  filetypes=[("CSV", "*.csv")])
    file = project.filename
    return file


def import_csv():
    csv_file = open(choose_file())
    my_csv = csv.reader(csv_file)
    for row in my_csv:
        print(row)


import_csv()
