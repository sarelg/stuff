# This script will pickle the pixel mask and the ivar for every object

import pickle
from os import listdir
import pyfits as pf
from deredshift import deredshift
from multiprocessing import Pool
import logging
import time

start = time.time()

logging.basicConfig(filename='mask_ivar.log', level=logging.INFO, format='%(levelname)s: %(message)s')

path = '/mnt/gastro/sarel/sdss/files/'

# list the files in the folder
fnames = listdir(path)
del fnames[0]


def ivar_mas(file_name, rel_data):
    # get the number of exposures for each file
    num_exp = int((pf.getheader(path+'%s' % file_name, 0)['nexp']) / 2)
    data = [0]*num_exp

    # run for each exposure
    for i in range(num_exp):

        # the tuples are there to save both the blue and the red part seperately,
        # both deredshifted to their rest frame values
        b_wl = 10 ** pf.getdata(path+'%s' % file_name, i + 4)['loglam']
        r_wl = 10 ** pf.getdata(path+'%s' % file_name, i + 4 + num_exp)['loglam']

        b_dat = pf.getdata(path+'%s' % file_name, i + 4)['%s' % rel_data]
        r_dat = pf.getdata(path+'%s' % file_name, i + 4 + num_exp)['%s' % rel_data]

        # we need to reverse the arrays if needed
        if b_wl[0] > b_wl[1]:
            b_wl = b_wl[::-1]
            b_dat = b_dat[::-1]

        if r_wl[0] > r_wl[1]:
            r_wl = r_wl[::-1]
            r_dat = r_dat[::-1]

        tup_blue = [deredshift(path+'%s' % file_name, b_wl), b_dat]
        tup_red = [deredshift(path+'%s' % file_name, r_wl), r_dat]
        data[i] = [tup_blue, tup_red]

    # the data structure looks like this: a file contains one object >> 4 sub exposures >>
    #  2 spectral parts, blue and red >> 2 vectors, the x axis and the pixel mask (ivar).
    return data


# create another function to actually pickle the data into folders (need a function for Pool)
def pick_l(data):
    try:
        mask = ivar_mas(data, 'mask')
        ivar = ivar_mas(data, 'ivar')
        pickle.dump(mask, open('/mnt/gastro/sarel/sdss/no_smooth/mask/%s.p' % data, 'wb'))
        pickle.dump(ivar, open('/mnt/gastro/sarel/sdss/no_smooth/ivar/%s.p' % data, 'wb'))
        logging.info('%s done' % data)
    except Exception:
        logging.error('problem with %s' % data)

# now divide it to all available processors
pool = Pool(processes=None)
pool.map(pick_l, fnames)

pool.close()
pool.join()

print('it took', (time.time() - start)/60, 'minutes')