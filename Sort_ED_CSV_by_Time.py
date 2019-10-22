# Order an Event Detection CSV File by Time
import csv
from operator import itemgetter
from tkinter import filedialog, Tk


def choose_file():
    project = Tk()
    project.filename = filedialog.askopenfilename(initialdir="/", title="Choose an IDPS CSV file",
                                                  filetypes=[("CSV", "*.csv")])
    file = project.filename
    return file


def parse_csv():
    csv_file = open(choose_file())
    my_csv = csv.reader(csv_file)
    parsed_csv = list(my_csv)
    header = parsed_csv[0]
    for index1, row in enumerate(parsed_csv):
        for index2, item in enumerate(row):
            try:
                parsed_csv[index1][index2] = (float(item))
            except ValueError:
                pass
    csv_list = sorted(parsed_csv[1:], key=itemgetter(0))
    for rows in csv_list:
        print(rows)
    csv_list.insert(0, header)
    with open('Ordered_EDs.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_list)


parse_csv()
