import pandas as pd
from numpy import *
from operantanalysis import *
from tkinter import filedialog, Tk


def choose_file():
    project = Tk()
    project.filename = filedialog.askopenfilename(initialdir="/", title="Choose an IDPS CSV file",
                                                  filetypes=[("CSV", "*.csv")])
    file = project.filename
    print("IDPS File:" + file)
    return file


def parse_csv():
    csv_file = open(choose_file())

    return csv_file


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
    event_detection_file = parse_csv()
    time_codes = list(map(float, behavior_file[0]))
    behaviors = list(behavior_file[1])
    df = pd.read_csv(event_detection_file, low_memory=False)
    df2 = pd.DataFrame(list(zip(time_codes, behaviors)), columns=['Time Codes', 'Behavior'])
    print(df2)

    df.columns = df.columns.astype(str)
    df.insert(df.shape[1], 'Reward', NaN)
    df.insert(df.shape[1], 'ITI', NaN)
    df.insert(df.shape[1], 'Go', NaN)
    df.insert(df.shape[1], 'Lever Press', NaN)
    df.insert(df.shape[1], 'NoGo', NaN)
    print(list(df.columns.values))
    cell_times = list(map(float, df[' '][1:]))
    print(cell_times)
    print(time_codes)
    print(behaviors)
    # print(df.iloc[:, [0, -5]])
    # print(df[' '].index.values.tolist())
    i = 1
    # for index, row in df.iloc[1:, [0]].iterrows():
    #   print(round(float(row.values), 2))

    for index, value in enumerate(cell_times):
        print(index, round(value, 2))
        for index_2, value_2 in enumerate(time_codes):
            if round(value, 2) == value_2:
                print(True)
                print(index_2, value_2)
                if behaviors[index_2] == 'DipOff' and behaviors[index_2 - i] == 'PokeOff1' and behaviors[
                    index_2 - i + 1] == 'PokeOn1' and \
                        behaviors[index_2 - i + 2] == 'DipOn':
                    print(True)
                    df.iloc[index + 1, [-5]] = 1
                else:
                    i += 1
                    df.iloc[index + 1, [-5]] = 0

    with pd.option_context('display.max_rows', 200, 'display.max_columns', 50):
        print(df)

    return df


def output_csv_file():
    df = align_lists()
    project = Tk()
    project.directory = filedialog.askdirectory(initialdir="/", title="Choose an Output Directory")
    output_path = project.directory
    print('File Output:' + output_path)
    df.to_csv(output_path + '/aligned_cell_operant_behavior_df.csv')


output_csv_file()
