# This script will calculate the average S/N in the OIII line

import pickle
import numpy as np
from multiprocessing import Pool
import csv
from os import listdir
import time
import logging


def ivar_est(filename):

    try:
        data_ivar = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/ivar/%s' % filename, 'rb'))
        data_flux = pickle.load(open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sub_exposures/%s' % filename, 'rb'))

        flux_list = []
        sub_list = []
        for i in range(len(data_ivar)):
            for j in range(len(data_ivar[i][0][0])):
                if data_ivar[i][0][0][j] >= (5007-20):
                    xji = j
                    break

            for j in range(len(data_ivar[i][0][0])):
                if data_ivar[i][0][0][j] >= (5007 + 20):
                    xjf = j
                    break

            a = data_ivar[i][0][1][xji:(xjf + 1)]
            a = a[~np.isnan(a)]
            avg_ivar = np.mean(a)

            sub_list.append(avg_ivar)

            for j in range(len(data_flux[i][0])):
                if data_flux[i][0][j] >= (5007 - 20):
                    xfi = j
                    break

            for j in range(len(data_flux[i][0])):
                if data_flux[i][0][j] >= (5007 + 20):
                    xff = j
                    break


            b = data_flux[i][1][xfi:(xff + 1)]
            b = b[~np.isnan(b)]
            avg_flux = np.mean(b)

            flux_list.append(avg_flux)


        sn = np.mean(flux_list) * pow(np.mean(sub_list), 0.5)

        logging.info(filename + ' done')
        return filename, sn

    except Exception:

        logging.error('Problem with ' + filename)
        return ['Error']

if __name__ == '__main__':

    start = time.time()

    logging.basicConfig(filename='/mnt/gastro/sarel/sdss/no_smooth/excels/average_sn.log',
                        level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    # create the file to write into
    path = '/mnt/gastro/sarel/sdss/no_smooth/'
    writer = csv.writer(open(path + 'excels/average_sn.csv', 'w'))
    writer.writerow(['File name', 'avg_sn'])

    file_list = listdir('/mnt/gastro/sarel/sdss/no_smooth/none_trial/ivar/')

    # for every object in the list we need to get the file name and ivar
    pool = Pool(processes=16)
    for result in pool.map(ivar_est, file_list):
        writer.writerow(result)

    pool.close()
    pool.join()

    print('It took', (time.time() - start) / 60, 'Minutes')