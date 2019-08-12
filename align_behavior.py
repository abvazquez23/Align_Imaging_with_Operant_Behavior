import csv
from operantanalysis import *
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
    # for rows in csv_list:
    #   print(rows)
    csv_list.insert(0, header)
    with open('Ordered_EDs.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows(csv_list)
    return csv_list


def load_operant_file():
    file = load_file(
        r'\\dartfs-hpc\rc\lab\N\NautiyalK\Abraham Vazquez\Imaging\Mouse728_DS_TroughTrain2_2019_For_Imaging\Day 14\!2019-08-02_10h43m.Subject 0')
    file_info = extract_info_from_file(file, 500)
    # for i in range(len(file_info[0])):
    #   print('{:<8} {:>10}'.format(file_info[0][i], file_info[1][i]))
    return file_info


def align_lists():
    behavior_file = load_operant_file()
    event_detection_file = parse_csv()
    cells_aligned_behavior = [behavior_file, event_detection_file]
    print(len(event_detection_file))
    # for i in range(len(cells_aligned_behavior[1])):
    #   print('{:<8} {:>10} {:>10} {:>10} {:>10}'.format(cells_aligned_behavior[]))

    data_dict = {'Headers': [event_detection_file[0], 'Behavioral Time Code', 'Behavioral Event'], 'Cell Events':
                 event_detection_file, 'Behavior': behavior_file}


align_lists()
