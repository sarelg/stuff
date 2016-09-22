# from os import listdir
import pyfits as pf
import csv
import time
import logging
import multiprocessing as mp
import warnings

# import numpy as np
# import matplotlib.pyplot as plt
# from diff_expo_plot import cor_exp

start = time.time()
warnings.filterwarnings("ignore")
logging.basicConfig(filename='dev_est_z.log', level=logging.INFO, format='%(levelname)s: %(message)s')

fnames = []
f1 = open('/mnt/gastro/sarel/sdss/no_smooth/dev_est.csv', 'r')
reader = csv.reader(f1)
reader.__next__()
for row in reader:
    fnames.append(row[0])

f2 = open('/mnt/gastro/sarel/sdss/no_smooth/z_dev_est.csv', 'w')
writer = csv.writer(f2)
writer.writerow(['File Name', 'z'])


def get_z(fname):
    try:
        a = fname
        a = a.replace('.p', '')
        z = pf.getdata('/mnt/gastro/sarel/sdss/files/%s' % a, 2)['z']
        logging.info('%s done' % a)
        return fname, z[0]
    except Exception:
        logging.error('problem with %s' % a)
        return fname, 'problem with %s' % a

pool = mp.Pool(processes=None)
for result in pool.map(get_z, fnames):
    writer.writerow(result)

pool.close()
pool.join()

f1.close()
f2.close()

print('It took', (time.time() - start) / 60, 'minutes')

# f = csv.reader(open('./new_fits/boss400/oiii_num.csv'))
# f2 = csv.reader(open('./new_fits/boss400/z_boss400.csv'))
# column1 = []
# column2 = []
#
# for row in f:
#     column1.append(row[18])
# for row in f2:
#     column2.append(row[1])
#
# del column1[0]
# del column2[0]
#
# for i in range(len(column1)):
#     column1[i] = float(column1[i])
#
# for i in range(len(column2)):
#     column2[i] = float(column2[i])
#
# std_avg = np.asarray(column1)
# z = np.asarray(column2)
#
# print('It took', time.time() - start, 'seconds')
#
# plt.plot(z, std_avg, '.')
# plt.xlabel('z')
# plt.ylabel('std/EW')
# plt.show()

# print('It took', time.time() - start, 'seconds')
