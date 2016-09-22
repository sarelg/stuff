import pickle
import pyfits as pf
from os import listdir
from deredshift import deredshift

path = '/Users/sarelg/gastro/sdss/files/'
file_list = listdir(path)
del file_list[0]
del file_list[0]


def pickle_med(filename):

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

    pickle.dump(data, open('/Users/sarelg/gastro/sdss/no_smooth/none_trial/sdss_med/spectra/%s.p' % filename, 'wb'))
    pickle.dump(or_mask, open('/Users/sarelg/gastro/sdss/no_smooth/none_trial/sdss_med/and_mask/%s.p' % filename, 'wb'))
    pickle.dump(and_mask, open('/Users/sarelg/gastro/sdss/no_smooth/none_trial/sdss_med/or_mask/%s.p' % filename, 'wb'))

pickle_med('spec-2644-54210-0427.fits')