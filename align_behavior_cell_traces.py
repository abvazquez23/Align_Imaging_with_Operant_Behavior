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
    with pd.option_context('display.max_rows', 795, 'display.max_columns', 2):
        print(df2)

    df.columns = df.columns.astype(str)
    df.insert(df.shape[1], 'Reward', NaN)
    df.insert(df.shape[1], 'ITI', NaN)
    df.insert(df.shape[1], 'Go', NaN)
    df.insert(df.shape[1], 'Lever Press', NaN)
    df.insert(df.shape[1], 'NoGo', NaN)
    df.insert(df.shape[1], 'Head In', NaN)
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
            if round(value, 2) == round(value_2, 1):
                print(True)
                print(index_2, round(value_2, 1))
                print(behaviors[index_2])
                if behaviors[index_2] == 'DipOn' and behaviors[index_2 + i] == 'DipOff':  # reward
                    print(False)
                    df.iloc[index + 1, [-6]] = 0
                if behaviors[index_2] == 'DipOff' and behaviors[index_2 - i] == 'DipOn':  # reward
                    print(False)
                    df.iloc[index + 1, [-6]] = 0

                if behaviors[index_2] == 'PokeOn1' and behaviors[index_2 - i] == 'DipOn':  # reward
                    print(True)
                    df.iloc[index + 1, [-6]] = 1
                if behaviors[index_2] == 'PokeOff1' and behaviors[index_2 + i] == 'DipOn' \
                        and behaviors[index_2 - i - 1] == 'PokeOn1':  # reward
                    print(True)
                    df.iloc[index + 1, [-6]] = 1
                if behaviors[index_2] == 'PokeOn1' and behaviors[index_2 - i] == 'PokeOff1' \
                        and behaviors[index_2 - i - 1] == 'DipOn':  # reward
                    print(True)
                    df.iloc[index + 1, [-6]] = 1

                if behaviors[index_2] == 'SuccessfulNoGoTrial':  # Successful No Go  Trial
                    print(True)
                    df.iloc[index + 1, [-2]] = 1

                if behaviors[index_2] == 'SuccessfulGoTrial':  # Successful Go Trial
                    print(True)
                    df.iloc[index + 1, [-4]] = 1

                if behaviors[index_2] == 'LPressOn':  # lever press
                    print(True)
                    df.iloc[index + 1, [-3]] = 1

                if behaviors[index_2] == 'PokeOn1' and behaviors[index_2 + i] != 'PokeOff1':
                    print(True)
                    df.iloc[index + 1, [-1]] = 1
                    df.iloc[index + 2, [-1]] = 1
                    if behaviors[index_2 + i + 1] != 'PokeOff1':
                        df.iloc[index + 3, [-1]] = 1
                    if behaviors[index_2 + i + 2] != 'PokeOff1':
                        print(True)
                        df.iloc[index + 4, [-1]] = 1

                    # if behaviors[index_2 + i + 3] != 'PokeOff1' or behaviors[index_2 + i + 3] == 'EndSession':
                    #   df.iloc[index + 5, [-1]] = 1

                # k = 2
                # if behaviors[index_2 + i + x] != 'PokeOff1':
                #   print(x)
                #  while True:
                #     df.iloc[index + k, [-1]] = 1
                #    x += 1
                #   k += 1
                #  if behaviors[index_2 + i + k] == 'PokeOff1':
                #     break
                #      if behaviors[index_2 + i] == 'PokeOff1':
                #         print(True)
                #        df.iloc[index + 1, [-5]] = 1

                # else:
                #   df.iloc[index + 1, [-5]] = 1
    # df.fillna(0, inplace=True)

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
