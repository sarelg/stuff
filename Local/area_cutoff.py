# This code will set the noise cutoff for the area

import csv
import pickle
import numpy as np


def cutoff(num):
    file_list = []
    with open('/Users/sarelg/gastro/sdss/no_smooth/excels/average_sn.csv', 'r') as csvfile:
        f = csv.reader(csvfile)
        f.__next__()
        for row in f:
            file_list.append(row[0])

    files = []
    for i in range(num):
        files.append(file_list[i])

    writer = csv.writer(open('/Users/sarelg/gastro/sdss/no_smooth/excels/100.csv', 'w'))
    writer.writerow(['File name', 'Area', 'Z'])

    c = open('/Users/sarelg/gastro/sdss/no_smooth/excels/area_under_subtraction_normalized_med.csv', 'r')
    reader = csv.reader(c)
    not_found = 0
    for i in range(len(files)):
        for row in reader:
            if files[i] == row[0]:
                writer.writerow(row)
                c.seek(0)
                break
            elif row[0] == 'Error':
                c.seek(0)
                not_found = not_found + 1
                break

    return not_found

print(cutoff(100))