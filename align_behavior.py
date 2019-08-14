import csv
from numpy import *
from operantanalysis import *
from operator import itemgetter
from tkinter import filedialog, Tk
from itertools import zip_longest


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
    file = load_file(
        r'\\dartfs-hpc\rc\lab\N\NautiyalK\Abraham Vazquez\Imaging\Mouse728_DS_TroughTrain2_2019_For_Imaging\Day 14\!2019-08-02_10h43m.Subject 0')
    file_info = extract_info_from_file(file, 500)
    return file_info


def align_lists():
    behavior_file = array(load_operant_file())
    event_detection_file = array(parse_csv())
    time_codes = list(behavior_file[0])
    behaviors = list(behavior_file[1])
    cell_time = list(event_detection_file[1:, 0])
    cell_number = list(event_detection_file[1:, 1])
    cell_value = list(event_detection_file[1:, 2])
    cell_header = list(event_detection_file[0])
    behavior_header = ['Behavior Time Code (s)', 'Behavioral Event']
    header = behavior_header + cell_header
    aligned_list = [header, time_codes, behaviors, cell_time, cell_number, cell_value]
    print(aligned_list)

    cell_and_behavior_time = sorted((time_codes + cell_time), key=float)
    # print(header)
    # for t, u, w, x, y,  z in zip_longest(cell_and_behavior_time, time_codes, behaviors, cell_time, cell_number, cell_value):
    #   print(t, u, w, x, y, z)
    print(cell_and_behavior_time)
    print(event_detection_file)
    for i in cell_and_behavior_time:
        for x in event_detection_file[1:, 0]:
            if x.any() == i:
                cell_and_behavior_time.append(event_detection_file[1:, 1:2])
    print(cell_and_behavior_time)
    data_dict = {'Headers': [event_detection_file[0], 'Behavioral Time Code (s)', 'Behavioral Event'],
                 'Cell_Number': event_detection_file[1:, 1], 'Cell_Time': event_detection_file[1:, 0],
                 'Cell_Value': event_detection_file[1:, 2],
                 'Behavior': behavior_file[1], 'Time_Code': behavior_file[0]}

    # with open('aligned_cell_behavior.csv', mode='w') as csvFile:
    #   fieldnames = ['Headers', 'Cell_Number', 'Cell_Time', 'Cell_Value', 'Behavior', 'Time_Code']
    #  writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    # writer.writeheader()
    # for data in data_dict:
    #   writer.writerow(data)


align_lists()
