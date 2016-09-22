import pickle
import pyfits as pf
from os import listdir
from deredshift import deredshift
import time
import logging
from multiprocessing import Pool


def pickle_med(filename):

    try:

        wl = 10 ** pf.getdata(path + filename, 1)['loglam']
        flux = pf.getdata(path + filename, 1)['flux']
        or_mask = pf.getdata(path + filename, 1)['or_mask']
        and_mask = pf.getdata(path + filename, 1)['and_mask']

        if wl[0] > wl[1]:
            flux = flux[::-1]
            wl = wl[::-1]

        wl = deredshift(path + filename, wl)

        data = [wl, flux]
        or_mask = [wl, or_mask]
        and_mask = [wl, and_mask]

        pickle.dump(data, open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sdss_med/spectra/%s.p' % filename, 'wb'))
        pickle.dump(or_mask, open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sdss_med/and_mask/%s.p' % filename, 'wb'))
        pickle.dump(and_mask, open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sdss_med/or_mask/%s.p' % filename, 'wb'))
        logging.info(filename + ' done')

    except Exception:

        print('Error with %s' % filename)
        logging.error('Problem with ' + filename)


if __name__ == '__main__':

    start = time.time()

    logging.basicConfig(filename='/mnt/gastro/sarel/sdss/no_smooth/excels/pickle_med.log',
                        level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    path = '/mnt/gastro/sarel/sdss/files/'
    file_list = listdir(path)
    del file_list[0]
    del file_list[0]

    # for every object in the list we need to get the file name and ivar
    pool = Pool(processes=16)
    pool.map(pickle_med, file_list)

    pool.close()
    pool.join()

    print('It took', (time.time() - start) / 60, 'Minutes')