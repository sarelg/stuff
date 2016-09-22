# This code will extract the seeing 50 for every exposure

import pyfits as pf
import pickle
import numpy as np


def seeing(filename):

    # get the number of exposures
    path = '/Users/sarelg/gastro/sdss/files/'
    num_exp = int((pf.getheader(path + filename, 0)['nexp'])/2)

    # put the seeing50 of all sub exposures in a list for every object
    seeing50 = []
    for i in range(num_exp):
        seeing50.append(pf.getheader(path + filename, 4 + i)['seeing50'])

    return filename, seeing50

print(seeing('spec-2644-54210-0427.fits'))