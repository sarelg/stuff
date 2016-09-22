# this script will attempt to estimate the typical variation of lines in the two known objects

import pickle
# import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
from os import listdir
import logging
import time
import csv

start = time.time()

logging.basicConfig(filename='/mnt/gastro/sarel/sdss/no_smooth/dev_est.log', level=logging.INFO, format='%(levelname)s: %(message)s')

writer = csv.writer(open('/mnt/gastro/sarel/sdss/no_smooth/dev_est.csv', 'w'))
writer.writerow(['Name', 'Line', 'Noise'])
path = '/mnt/gastro/sarel/sdss/no_smooth/after_division'
dir_list = listdir('%s' % path)
# del dir_list[0]
# del dir_list[0]


def var_est(file_name):

    # open the data
    try:
        data = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/after_division/%s' % file_name, 'rb'))

    # find out where the OIII line is
        for i in range(len(data[0][0])):
            if data[0][0][i] >= (5007 - 5):
                    xfi = i
                    break

        for i in range(len(data[0][0])):
            if data[0][0][i] >= (5007 + 5):
                xff = i
                break

        # make a list of the averages for each exposure
        avg = []
        for i in range(len(data)):
            avg.append(np.mean(data[i][1][xfi:(xff+1)]))

        # get the variations for each exposure and the ones next to it
        avg_pct = []
        for i in range(len(data) - 1):
            if ((avg[i+1]/avg[i] - 1)*100) < 0:
                avg_pct.append((avg[i]/avg[i+1] - 1)*100)
            else:
                avg_pct.append((avg[i+1] / avg[i] - 1) * 100)
        # and this is the maximum variation
        line_max_dev = (max(avg)/min(avg) - 1)*100

        # now get the variations of the noise
        for i in range(len(data[0][0])):
            if data[0][0][i] >= (4800 - 5):
                    xfi = i
                    break

        for i in range(len(data[0][0])):
            if data[0][0][i] >= (4800 + 5):
                xff = i
                break

        avg = []
        for i in range(len(data)):
            avg.append(np.mean(data[i][1][xfi:(xff+1)]))

        avg_pct = []
        for i in range(len(data) - 1):
            if ((avg[i+1]/avg[i] - 1)*100) < 0:
                avg_pct.append((avg[i] / avg[i+1] - 1) * 100)
            else:
                avg_pct.append((avg[i+1] / avg[i] - 1) * 100)
        noise_max_dev = (max(avg)/min(avg) - 1)*100

        # print('%s done' % file_name)
        return file_name, line_max_dev, noise_max_dev

    except Exception:
        logging.error('problem with %s' % file_name)
        print('problem with %s' % file_name)

        return '%s' % file_name, 'problem with %s' % file_name

pool = Pool(processes=None)
for result in pool.map(var_est, dir_list):
    writer.writerow(result)
pool.close()
pool.join()

print('It took', time.time() - start, 'seconds')