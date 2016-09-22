# this script chooses a random object and plots its oiii fit
import matplotlib.pyplot as plt
from os import listdir
import random
import pyfits as pf
import pickle
from multiprocessing import Pool


# take the function that fits a gaussian to the OIII line but plot it
def oiii(data):
    import astropy.modeling as mod
    import numpy as np
    import scipy.integrate as int
    import matplotlib.pyplot as plt
    from EW_lines import continuum

    x = data[0]
    y = data[1]

    # subtract the contiuum
    y = continuum(x, y)

    # isolate the OIII line
    for i in range(len(x)):
        if x[i] >= (5007 - 30):
            xfi = i
            break

    for i in range(len(x)):
        if x[i] >= (5007 + 30):
            xff = i
            break

    x1 = np.zeros(abs(xff - xfi))
    y1 = np.zeros(abs(xff - xfi))

    for i in range(len(x1)):
        x1[i] = x[xfi + i]
        y1[i] = y[xfi + i]

    # define the gaussian for the fit
    def cus_gauss(x, amplitude=1., mean=0., stddev=1.):
        return 1 + amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    cus_mod = mod.models.custom_model(cus_gauss)

    # find out where the 5007 line is exactly and take the
    # amplitude for the initial guess
    for i in range(len(x)):
        if x[i] >= 5007:
            x_line = i
            break

    # perform the fit
    g_init = cus_mod(y[x_line], 5007, 1)
    fit_g = mod.fitting.LevMarLSQFitter()
    # g_init.mean.fixed = True
    g_init.amplitude.bounds = [0, 1000]
    g_init.mean.bounds = [5002, 5012]
    g = fit_g(g_init, x1, y1)

    # calcualte the equivalent width
    def integrand(x, amplitude, mean, stddev):
        return amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    xfit = np.arange(0., 10000., 1.)
    yfit = integrand(xfit, g.amplitude, g.mean, g.stddev)
    equwid = (int.simps(yfit))
    plt.figure()
    plt.plot(x1, y1)
    plt.plot(x1, g(x1))
    plt.show()

    return equwid

# list the objects
list1 = listdir('/Users/sarelg/gastro/sdss/after_division/')

# pick a random object, keep picking randomly until it has a redshift of over 0.15
a = random.choice(list1)
b = a.replace('.p', '')
while pf.getdata('/Users/sarelg/gastro/sdss/files/%s' % b, 2)['z'] < 0.15:
    a = random.choice(list1)
    b = a.replace('.p', '')
print(pf.getdata('/Users/sarelg/gastro/sdss/files/%s' % b, 2)['z'])
# a = 'spec-1704-53178-0481.fits.p'
data = pickle.load(open('/Users/sarelg/gastro/sdss/after_division/%s' % a, 'rb'))

# plot all the subexposures
pool = Pool(processes=None)
pool.map(oiii, data)

pool.close()
pool.join()
