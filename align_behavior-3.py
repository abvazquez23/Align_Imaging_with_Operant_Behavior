import csv
import pandas as pd
from numpy import *
from operantanalysis import *
from operator import itemgetter
from tkinter import filedialog, Tk
from matplotlib import pyplot as plt


def choose_file():
    project = Tk()
    project.filename = filedialog.askopenfilename(initialdir="/", title="Choose an IDPS CSV file",
                                                  filetypes=[("CSV", "*.csv")])
    file = project.filename
    print("IDPS File:" + file)
    return file


def parse_csv():
    csv_file = open(choose_file())
    my_csv = csv.reader(csv_file)
    parsed_csv = list(my_csv)
    header = parsed_csv[0]
    for index1, row in enumerate(parsed_csv):
        for index2, item in enumerate(row):
            try:
                parsed_csv[index1][index2] = round((float(item)), 2)
            except ValueError:
                pass
    csv_list = sorted(parsed_csv[1:], key=itemgetter(0))
    csv_list.insert(0, header)
    with open('Ordered_EDs.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows(csv_list)
    return csv_list


def load_operant_file():
    project = Tk()
    project.filename = filedialog.askopenfilename(initialdir="/", title="Choose a Behavioral Operant File",
                                                  filetypes=[("all files", "*.")])
    operant_file = project.filename
    print("Operant File:" + operant_file)
    file = load_file(operant_file)
    file_info = extract_info_from_file(file, 500)
    return file_info


def align_lists():
    behavior_file = array(load_operant_file())
    event_detection_file = array(parse_csv())
    a = 0.00
    time_codes = list(map(float, behavior_file[0]))
    behaviors = list(behavior_file[1])
    cell_time = [a] + list(map(float, event_detection_file[1:, 0]))
    cell_name = [a] + list(event_detection_file[1:, 1])
    cell_value = [a] + list(event_detection_file[1:, 2])
    df = pd.DataFrame(list(zip(cell_time, cell_name, cell_value)), columns=['Time (s)', 'Cell Name', 'Cell Value'])
    df2 = pd.DataFrame(list(zip(time_codes, behaviors)), columns=['Time Codes', 'Behavior'])
    print(df2)
    df.insert(3, 'Time Codes', NaN)
    df.insert(4, 'Behavior', NaN)
    matched_array = df['Time (s)'].searchsorted(df2['Time Codes'])
    for x in range(len(matched_array)):
        df.loc[matched_array[x], 'Time Codes'] = time_codes[x]
        df.loc[matched_array[x], 'Behavior'] = behaviors[x]
    df['Behavior'].fillna(method='ffill', inplace=True)
    df_pivot = df.pivot(index='Time (s)', columns='Cell Name', values='Cell Value')
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):
        print(df_pivot)

    return df_pivot


def output_csv_file():
    df = align_lists()
    project = Tk()
    project.directory = filedialog.askdirectory(initialdir="/", title="Choose an Output Directory")
    output_path = project.directory
    print('File Output:' + output_path)
    df.to_csv(output_path + '/aligned_cell_operant_behavior.csv')


output_csv_file()

