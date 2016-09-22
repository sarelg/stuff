# this script will divide the lines of different exposures and plot the divisions.

import pickle
import numpy as np
from multiprocessing import Pool
import csv
import pyfits as pf
import logging
import time
from os import listdir


def plot_var(file_name, none=False):

    # open the data
    if none == False:
        data = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/after_division/%s' % file_name, 'rb'))
    else:
        data = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sub_exposures/%s' % file_name, 'rb'))

    all_exp = []
    for i in range(len(data)):
        # get the OIII line
        for j in range(len(data[i][0])):
            if data[i][0][j] >= (5007 - 20):
                xfi = j
                break

        for j in range(len(data[i][0])):
            if data[i][0][j] >= (5007 + 20):
                xff = j
                break

        # make a list for each exposure of the pixels around the line
        a = np.asarray(data[i][1][xfi:(xff+1)])
        all_exp.append(a)

    return all_exp


def sorti(filename, data):

    # make a list of the maximum value of each exposure
    sorti = []
    for i in range(len(data)):
        sorti.append(max(data[i]))

    # find out which exposure is the min and which is the max
    min1, max1 = np.argmin(sorti), np.argmax(sorti)

    # make the subtracted vector and ignore the NaNs
    vec = data[max1] - data[min1]
    vec = vec[~np.isnan(vec)]

    # calculate the area
    area = np.trapz(vec)

    med = np.median([data[max1], data[min1]], axis=0)
    med = med[~np.isnan(med)]
    # becuase we aren't dividing but subtracting, and using the none normalized sub exposures, we need to normalize
    # the area

    area /= np.trapz(med)

    if np.isnan(area):
        area = 0.0

    # get the seeing50 difference between the two exposures
    filesee = filename.replace('.p', '')
    seemax = pf.getheader('/mnt/gastro/sarel/sdss/files/%s' % filesee, 4 + max1)['seeing50']
    seemin = pf.getheader('/mnt/gastro/sarel/sdss/files/%s' % filesee, 4 + min1)['seeing50']

    seeing_diff = seemin - seemax
    marked = False
    if float(seemin) > 3 and float(seemax) < 3:
        marked = True
    elif float(seemax) > 3 and float(seemin) < 3:
        marked = True

    return area, seeing_diff, marked


def main(filename):

    try:
        # get the area
        data = plot_var(filename, none=True)
        area, seeing_diff, marked = sorti(filename, data)

        # get the redshift
        filez = filename.replace('.p', '')
        z = pf.getdata('/mnt/gastro/sarel/sdss/files/%s' % filez, 2)['z']

        logging.info(filename + ' done')
        return filename, area, seeing_diff, z[0], marked

    except Exception:

        logging.error('Problem with ' + filename)
        return ['Error']


if __name__ == '__main__':

    start = time.time()

    logging.basicConfig(filename='/mnt/gastro/sarel/sdss/no_smooth/excels/area_under_sub+seeing50_markedboth.log', level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    # create the file to write into
    path = '/mnt/gastro/sarel/sdss/no_smooth/'
    writer = csv.writer(open(path + 'excels/area_under_sub+seeing50_markedboth.csv', 'w'))
    writer.writerow(['File name', 'Area', 'Seeing 50', 'Z', 'Marked'])

    file_list = listdir('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sub_exposures/')
    del(file_list[0])

    # for every object in the list we need to get the file name, area, seeing and z
    pool = Pool(processes=16)
    for result in pool.map(main, file_list):
        writer.writerow(result)

    pool.close()
    pool.join()

    print('It took', (time.time() - start)/60, 'Minutes' )