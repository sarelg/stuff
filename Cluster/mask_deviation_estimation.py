# this script will attempt to estimate the typical variation of lines in all the objects

import pickle
# import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
from os import listdir
import logging
import time
import csv

start = time.time()

logging.basicConfig(filename='./dev_est_mask.log', level=logging.INFO, format='%(levelname)s: %(message)s')

writer = csv.writer(open('./dev_est_mask.csv', 'w'))
writer.writerow(['File Name', 'Line', 'Noise', 'Bad'])
path = '/mnt/gastro/sarel/sdss/no_smooth/after_division'
dir_list = listdir('%s' % path)
del dir_list[0]


def var_est(file_name):

    try:
        # open the data
        data = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/after_division/%s' % file_name, 'rb'))
        data_mask = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/mask/%s' % file_name, 'rb'))

        # find out where the OIII line is
        for i in range(len(data[0][0])):
            if data[0][0][i] >= (5007 - 5):
                xfi = i
                break

        for i in range(len(data[0][0])):
            if data[0][0][i] >= (5007 + 5):
                xff = i
                break

        # and now find out where the line is for the masks
        for i in range(len(data_mask[0][1][0])):
            # if data[0][0][0][i] >= (5700 - 5):
            #     xfi_mask = i
            #     break
            if data_mask[0][1][0][i] >= (5700 - 5):
                xfi_mask = i
                break
        for i in range(len(data_mask[0][1][0])):
            # if data[0][0][0][i] >= (5700 + 5):
            #     xff_mask = i
            #     break
            if data_mask[0][1][0][i] >= (5700 + 5):
                xff_mask = i
                break

        # make a list of the averages for each exposure
        avg = []
        avg_mask = []
        for i in range(len(data)):
            avg.append(np.mean(data[i][1][xfi:(xff+1)]))
            # now check to see whether the mask of each exposure removes pixels in the relevant area
            counter = 0
            for j in range(xff_mask - xfi_mask):
                if data_mask[i][1][1][j] != 0:
                   counter =+ 1
            if counter == 0:
                avg_mask.append(False)
            else:
                avg_mask.append(True)

        for i in range(len(avg_mask)):
            if avg_mask[i] == True:
                bad = True
                break
            else:
                bad = False

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

        # put the results in a list
        avg = []
        for i in range(len(data)):
            avg.append(np.mean(data[i][1][xfi:(xff+1)]))

        avg_pct = []
        for i in range(len(data) - 1):
            if ((avg[i+1]/avg[i] - 1)*100) < 0:
                avg_pct.append((avg[i] / avg[i+1] - 1) * 100)
            else:
                avg_pct.append((avg[i+1] / avg[i] - 1) * 100)

        # maximum noise variation
        noise_max_dev = (max(avg)/min(avg) - 1)*100
        logging.info('%s done' % file_name)

        return file_name, line_max_dev, noise_max_dev, bad

    except Exception:
        logging.error('problem with %s' % file_name)

        return file_name, ['Error'], ['Error'], ['Error']

pool = Pool(processes=None)
for result in pool.map(var_est, dir_list):
    writer.writerow(result)
pool.close()
pool.join()

print('It took', time.time() - start, 'seconds')