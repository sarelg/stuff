from diff_expo_plot import cor_exp
from EW_lines import oiii, SN
import csv
from os import listdir
import numpy as np

# make a list of the file names and delete the first file (hidden)
fnames = listdir('./fits/exc_trial')
del fnames[0]


# make a function that gives a list of EW of a file
def ewlist(fname):
    data = cor_exp(fname)
    ew_exp = [0]*len(data)
    for i in range(len(data)):
        ew_exp[i] = oiii(data[i][0], data[i][1])[0]
    ew_exp.insert(0, fname)
    return ew_exp

def SNlist(fname):
    data = cor_exp(fname)
    sn_exp = [0]*len(data)
    for i in range(len(data)):
        sn_exp[i] = SN(data[i][0], data[i][1], 3737)
    sn_exp.insert(0, fname)
    return sn_exp

# write the labels in the csv files
fl = open('oiii_2.csv', 'w')
writer = csv.writer(fl)
writer.writerow(['File Name', 'Exp 1', 'Exp 2', 'Exp 3', 'Exp 4',
                     'Exp 5', 'Exp 6', 'Exp 7', 'Exp 8', 'Exp 9'])

fl2 = open('oiii_2 problems.csv', 'w')
writer2 = csv.writer(fl2)
writer2.writerow(['problematic files'])

fl3 = open('oiii_2 SN.csv', 'w')
writer3 = csv.writer(fl3)
writer3.writerow(['File Name', 'S/N'])

# loop through the files and insert into the csv, files who's standard
# deviation exceeds 100 will not be written in
for i in range(len(fnames)):
    try:
        list1 = ewlist(fnames[i])
        std_list=[]
        for j in range(1,len(list1)):
            std_list.append(list1[j])
        if np.std(std_list) < 30:
            writer.writerow(list1)
            writer3.writerow(SNlist(fnames[i]))
        else:
            writer2.writerow([fnames[i]])
    except Exception:
        writer2.writerow([fnames[i]])
        '''print('Problem with %s' % fnames[i])'''

fl.close()







