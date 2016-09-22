from diff_expo_plot import cor_exp
import pickle
from os import listdir
from EW_lines import continuum
import numpy as np
from multiprocessing import Pool
import time
import logging
import warnings


# pickle to three different folders the continuum fits, divided spectra and raw fits
def pickl(fname):
    try:
        cor = cor_exp(fname)
        sub_con = np.copy(cor)
        sub_fit = np.copy(cor)
        pickle.dump(cor, open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/sub_exposures/%s.p' % fname, 'wb'))
        for j in range(len(sub_con)):
            sub_con[j][1], sub_fit[j][1] = continuum(cor[j][0], cor[j][1], is_new=True)
        pickle.dump(sub_con, open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/after_division/%s.p' % fname, 'wb'))
        pickle.dump(sub_fit, open('/mnt/gastro/sarel/sdss/no_smooth/none_trial/just_cont/%s.p' % fname, 'wb'))
        logging.info('%s done' % fname)
    except Exception:
        logging.error('Problem with %s' % fname)

if __name__ == '__main__':

    start = time.time()
    warnings.filterwarnings("ignore")
    logging.basicConfig(filename='pickle_none.log', level=logging.INFO, format='%(levelname)s: %(message)s')

    # list all the files in the folder
    fnames = listdir('/mnt/gastro/sarel/sdss/files')
    del fnames[0]
    del fnames[0]

    pool = Pool(processes=None)
    pool.map(pickl, fnames)

    pool.close()
    pool.join()

    print('It took', (time.time() - start) / 60, 'minutes')
