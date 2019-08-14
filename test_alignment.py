from operantanalysis import *
import csv

file = load_file(r'\\dartfs-hpc\rc\lab\N\NautiyalK\Abraham Vazquez\Imaging\Mouse728_DS_TroughTrain2_2019_For_Imaging\Day 14\!2019-08-02_10h43m.Subject 0')
file_info = extract_info_from_file(file, 500)


print(file)
# print(file_info)
# print(file_info[0])
# print(file_info[1])

for i in range(len(file_info[0])):
    print('{:<8} {:>10}'.format(file_info[0][i], file_info[1][i]))

behavior_dict = dict(Time_Codes= file_info[0], Behavior= file_info[1])
with open('behavioral_file.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Time_Codes', 'Behavior']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(behavior_dict)

