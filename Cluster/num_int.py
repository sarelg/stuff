from EW_lines import oiii_num
import csv
from os import listdir
# import numpy as np
import pickle
import time
import logging
from multiprocessing import Pool

start = time.time()

# define the log file
logging.basicConfig(filename='/mnt/gastro/sarel/sdss/no_smooth/num_int.log',
                    level=logging.INFO, format='%(levelname)s: %(message)s')

# make a list of the file names and delete the first file (hidden)
fnames = listdir('/mnt/gastro/sarel/sdss/no_smooth/after_division')


# make a function that gives a list of EW of a file
def ewlist(fname):
    data = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/after_division/%s' % fname, 'rb'))
    ew_exp = [0] * len(data)
    for i in range(len(data)):
        ew_exp[i] = oiii_num(data[i][0], data[i][1])
    ew_exp.insert(0, fname)
    return ew_exp

# def SNlist(fname):
#     data = pickle.load(open('./new_fits/after division/%s' % fname, 'rb'))
#     sn_exp = [0] * len(data)
#     for i in range(len(data)):
#         sn_exp[i] = SN(data[i][0], data[i][1], 3737)
#     sn_exp.insert(0, fname)
#     sn_avg = np.average(sn_exp[1:len(sn_exp)])
#     return sn_exp, sn_avg


# write the labels in the csv files

fl = open('/mnt/gastro/sarel/sdss/no_smooth/oiii_num.csv', 'w')
writer = csv.writer(fl)
writer.writerow(['File Name', 'Exp 1', 'Exp 2', 'Exp 3', 'Exp 4',
                 'Exp 5', 'Exp 6', 'Exp 7', 'Exp 8', 'Exp 9', 'Exp 10',
                 'Exp 11', 'Exp12'])

fl2 = open('/mnt/gastro/sarel/sdss/no_smooth/oiii_num problems.csv', 'w')
writer2 = csv.writer(fl2)
writer2.writerow(['problematic files'])


# loop through the files and insert into the csv
def num_do(fname):
    try:
        list1 = ewlist(fname)
        logging.info('%s done' % fname)
        return list1
    # std_list = []
    # for j in range(1, len(list1)):
    #     std_list.append(list1[j])
    # std = np.std(std_list)
    # average = np.average(std_list)

    except Exception:
        writer2.writerow([fname])
        logging.error('Problem with %s' % fname)

# run on all processors and insert results into csv
pool = Pool(processes=None)
for result in pool.map(num_do, fnames):
    writer.writerow(result)

pool.close()
pool.join()

fl.close()
fl2.close()

print('It took', (time.time() - start)/60, 'minutes')
