from diff_expo_plot import cor_exp
import pickle
from os import listdir
from EW_lines import continuum
import numpy as np
from multiprocessing import Pool

# pickle to three different folders the continuum fits, divided spectra and raw fits
def pick_l(fname):
    # for i in range(len(fnames)):
        try:
            cor = cor_exp(fname)
            sub_con = np.copy(cor)
            sub_fit = np.copy(cor)
            pickle.dump(cor, open('./new_fits/sdss/no smooth/sub exposures/%s.p' % fname, 'wb'))
            for j in range(len(sub_con)):
                sub_con[j][1], sub_fit[j][1] = continuum(cor[j][0], cor[j][1], is_new=True)
            pickle.dump(sub_con, open('./new_fits/sdss/no smooth/after division/%s.p' % fname, 'wb'))
            pickle.dump(sub_fit, open('./new_fits/sdss/no smooth/just cont/%s.p' % fname, 'wb'))
            print('%s done' % fname)
        except Exception:
            print('Problem with %s' % fname)

if __name__ == '__main__':

    # list all the files in the folder
    fnames = listdir('./new_fits/sdss/files/')
    del fnames[0]

    pool = Pool(processes=None)
    pool.map(pick_l, fnames)

    pool.close()
    pool.join()