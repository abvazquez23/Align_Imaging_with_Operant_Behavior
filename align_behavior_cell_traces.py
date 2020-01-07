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
    df.insert(df.shape[1], 'Raw Behavioral Codes', NaN)
    df.insert(df.shape[1], 'Reward Presentation', NaN)
    df.insert(df.shape[1], 'Head In', NaN)
    df.insert(df.shape[1], 'Reward Retrieval', NaN)
    df.insert(df.shape[1], 'ITI', NaN)
    df.insert(df.shape[1], 'Lever Press', NaN)
    df.insert(df.shape[1], 'Go Trial', NaN)
    df.insert(df.shape[1], 'Successful Go Trial', NaN)
    df.insert(df.shape[1], 'No Go Trial', NaN)
    df.insert(df.shape[1], 'Successful No Go Trial', NaN)
    df.insert(df.shape[1], 'Unsuccessful No Go Trial', NaN)

    print(list(df.columns.values))
    cell_times = list(map(float, df[' '][1:]))

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            if round(value_2, 1) == value:
                print(True)
                print(index_2, value_2)
                print(behaviors[index_2])
                df.iloc[index + 1, [-11]] = str(behaviors[index_2])
                if behaviors[index_2] == 'DipOn':  # reward presentation
                    print(True)
                    df.iloc[index + 1, [-10]] = 1
                    x = 1
                    n = []
                    while True:
                        df.iloc[index + x, [-10]] = 1
                        x += 1
                        print(x)
                        t = round(float(df2.iat[index_2 + x, 0]), 1)
                        print(t)
                        try:
                            print(cell_times.index(t))
                            n.append(cell_times.index(t))
                            print(n)
                            print(list(range(n[0], n[-1] + 1)))
                        except:
                            ValueError
                        try:
                            for y in list(range(n[0], n[-1] + 1)):
                                df.iloc[y + 1, [-10]] = 1
                            df.iloc[n[-1] + 1, [-10]] = 1
                        except:
                            ValueError
                        if behaviors[index_2 + x] == 'DipOff':
                            break

                    if behaviors[index_2] == 'DipOn' and behaviors[index_2 + 1] != 'DipOff' \
                            and behaviors[index_2 - 1] != 'PokeOn1':  # reward retrieval
                        print(True)
                        x = 1
                        n = []
                        while True:
                            x += 1
                            print(x)
                            t = round(float(df2.iat[index_2 + x, 0]), 1)
                            print(t)
                            try:
                                print(cell_times.index(t))
                                n.append(cell_times.index(t))
                                print(n)
                                print(list(range(n[0], n[-1] + 1)))
                            except:
                                ValueError
                            try:
                                for y in list(range(n[0], n[-1] + 1)):
                                    df.iloc[y + 1, [-8]] = 0
                                df.iloc[n[-1] + 1, [-8]] = 1
                            except:
                                ValueError
                            if behaviors[index_2 + x] == 'PokeOn1':
                                break

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            if round(value_2, 1) == value:
                if behaviors[index_2] == 'SuccessfulNoGoTrial':  # Successful No Go  Trial
                    print(True)
                    df.iloc[index + 1, [-2]] = 1

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            if round(value_2, 1) == value:
                if behaviors[index_2] == 'SuccessfulGoTrial':  # Successful Go Trial
                    print(True)
                    df.iloc[index + 1, [-4]] = 1

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            if round(value_2, 1) == value:
                if behaviors[index_2] == 'LPressOn':  # lever press
                    print(True)
                    df.iloc[index + 1, [-3]] = 1

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            if round(value_2, 1) == value:
                if behaviors[index_2] == 'PokeOn1' and behaviors[index_2 + 1] == 'DipOn':  # reward retrieval
                    print(True)
                    i = cell_times.index(round(float(df2.iat[index_2 + 3, 0]), 1))
                    print(i)
                    df.iloc[i, [-8]] = 1

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            if round(value_2, 1) == value:
                if behaviors[index_2] == 'PokeOn1':  # head in
                    print(True)
                    x = 0
                    n = [cell_times.index(round(float(df2.iat[index_2, 0]), 1))]
                    while True:
                        x += 1
                        print(x)
                        t = round(float(df2.iat[index_2 + x, 0]), 1)
                        print(t)
                        try:
                            print(cell_times.index(t))
                            n.append(cell_times.index(t))
                            print(n)
                            print(list(range(n[0], n[-1] + 1)))
                            for y in list(range(n[0] + 1, n[-1] + 1)):
                                df.iloc[y, [-9]] = 1
                            df.iloc[n[-1] + 1, [-9]] = 1
                        except:
                            ValueError
                        if behaviors[index_2 + x] == 'PokeOff1' or behaviors[index_2 + x] == 'EndSession':
                            print('Done')
                            break

    for index, value in enumerate(cell_times):
        for index_2, value_2 in enumerate(time_codes):
            df.iloc[index, [-7]] = 1
            if round(value_2, 1) == value:
                if behaviors[index_2] == 'DipOn':  # ITI
                    print(True)
                    df.iloc[index + 1, [-7]] = 0
                    x = 1
                    n = []
                    while True:
                        df.iloc[index + x, [-7]] = 0
                        x += 1
                        print(x)
                        t = round(float(df2.iat[index_2 + x, 0]), 1)
                        print(t)
                        try:
                            print(cell_times.index(t))
                            n.append(cell_times.index(t))
                            print(n)
                            print(list(range(n[0], n[-1] + 1)))
                        except:
                            ValueError
                        try:
                            for y in list(range(n[0], n[-1] + 1)):
                                df.iloc[y + 1, [-7]] = 0
                            df.iloc[n[-1] + 1, [-7]] = 0
                        except:
                            ValueError
                        if behaviors[index_2 + x] == 'DipOff':
                            break

                if behaviors[index_2] == 'LLeverOn':
                    print(True)
                    df.iloc[index + 1, [-7]] = 0
                    x = 1
                    n = []
                    while True:
                        df.iloc[index + x, [-7]] = 0
                        x += 1
                        print(x)
                        t = round(float(df2.iat[index_2 + x, 0]), 1)
                        print(t)
                        try:
                            print(cell_times.index(t))
                            n.append(cell_times.index(t))
                            print(n)
                            print(list(range(n[0], n[-1] + 1)))
                        except:
                            ValueError
                        try:
                            for y in list(range(n[0], n[-1] + 1)):
                                df.iloc[y + 1, [-7]] = 0
                            df.iloc[n[-1] + 1, [-7]] = 0
                        except:
                            ValueError
                        if behaviors[index_2 + x] == 'LLeverOff':
                            break

    df.fillna(0, inplace=True)

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
