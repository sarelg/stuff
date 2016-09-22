from os import listdir
import pyfits as pf
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from diff_expo_plot import cor_exp
#
start = time.time()
#
# fnames = listdir('./new_fits/boss400/after division')
# del fnames[0]
#
# fl = open('./new_fits/boss400/z_boss400.csv', 'w')
# writer = csv.writer(fl)
# writer.writerow(['File Name', 'z'])
#
# for i in range(len(fnames)):
#     a = fnames[i]
#     a = a.replace('.p', '')
#     z = pf.getdata('./new_fits/boss400/files/%s' % a, 2)['z']
#     writer.writerow([fnames[i], z[0]])
#
# fl.close()
#
f = csv.reader(open('./cluster/no_smooth/oiii_fit_num.csv'))
column1 = []
column2 = []
column3 = []
f.__next__()

for row in f:
    column1.append(row[19])
    column2.append(row[20])
    med_list = []
    try:
        for i in range(len(row)):
            if len(row[i+1]) == 0:
                break
            else:
                med_list.append(float(row[i+1]))
        median = np.median(med_list)
        mad = np.median(np.absolute(median - med_list))
        column3.append(mad/median)
    except Exception:
        column3.append(0)
for i in range(len(column1)):
    try:
        column1[i] = float(column1[i])
        column2[i] = float(column2[i])
        column3[i] = float(column3[i])
    except Exception:
        column1[i] = 0
        column2[i] = 0
        column3[i] = 0

std_avg = np.asarray(column1)
z = np.asarray(column2)
mad_med = np.asarray(column3)

print('It took', time.time() - start, 'seconds')

plt.plot(z, std_avg, '.b')
plt.plot(z, mad_med, '*g')
plt.xlabel('z')
plt.ylabel('std/EW')
# plt.ylim(ymax=0.1)
plt.show()

# f1 = open('./cluster/oiii_num.csv', 'r')
# f2 = open('./cluster/z_sdss.csv', 'r')
#
# reader1 = csv.reader(f1)
# reader2 = csv.reader(f2)
#
# num = []
# z = []
#
# for row in reader1:
#     num.append(row[0])
# for row in reader2:
#     z.append(row[0])
# del num[0]
# del z[0]
# del z[0]
#
# print(len(num), len(z))
