# this script will calculate the std/EW as a function of using a
# gaussian fit of the OIII emission line
from EW_lines import oiii
import csv
from os import listdir
import pickle
import time
import logging
from multiprocessing import Pool
import warnings

start = time.time()

# suppress warnings (astropy fit)
warnings.filterwarnings("ignore")

# define the log file
logging.basicConfig(filename='/mnt/gastro/sarel/sdss/no_smooth/num_fit.log',
                    level=logging.INFO, format='%(levelname)s: %(message)s')

# make a list of the file names and delete the first file (hidden)
fnames = listdir('/mnt/gastro/sarel/sdss/no_smooth/after_division')
# del fnames[0]

# write the labels in the csv files
fl = open('/mnt/gastro/sarel/sdss/no_smooth/oiii_fit_num.csv', 'w')
writer = csv.writer(fl)
writer.writerow(['File Name', 'Exp 1', 'Exp 2', 'Exp 3', 'Exp 4',
                 'Exp 5', 'Exp 6', 'Exp 7', 'Exp 8', 'Exp 9', 'Exp 10',
                 'Exp 11', 'Exp12'])

fl2 = open('/mnt/gastro/sarel/sdss/no_smooth/oiii_fit_num problems.csv', 'w')
writer2 = csv.writer(fl2)
writer2.writerow(['problematic files'])


# make a function that gives a list of EW of a file
def ewlist(fname):
    data = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/after_division/%s' % fname, 'rb'))
    ew_exp = [0] * len(data)
    for i in range(len(data)):
        ew_exp[i] = oiii(data[i][0], data[i][1])
    ew_exp.insert(0, fname)
    return ew_exp


def num_do(fname):
    # loop through the files and insert into the csv
    try:
        list1 = ewlist(fname)
        logging.info('%s done' % fname)
        return list1
    except Exception:
        writer2.writerow([fname])
        logging.error('Problem with %s' % fname)
        return 0

# run on all processors and insert results into csv
pool = Pool(processes=None)
for result in pool.map(num_do, fnames):
    if result != 0:
        writer.writerow(result)

pool.close()
pool.join()

fl.close()
fl2.close()

print('It took', (time.time() - start)/60, 'minutes')
