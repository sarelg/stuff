import pyfits as pf
import matplotlib.pyplot as plt
import numpy
import scipy.interpolate as inter
from math import ceil

# create the path of the fits file.
path_fits = './fits/spec-0491-51942-0001.fits'

# input all the data into different variables for ease of use.
# for now, two vars, one for the blue and one for the red.
b_data = pf.getdata(path_fits, 4)
r_data = pf.getdata(path_fits, 13)
b_flux = b_data['flux']
b_wl = 10 ** b_data['loglam']
r_flux = r_data['flux']
r_wl = 10 ** r_data['loglam']

# we need to reverse the arrays, notice that the red wavelength is not reversed (for some reason)
b_flux = b_flux[::-1]
b_wl = b_wl[::-1]

# we interpolate the blue and red parts so we can create one single continuum
b_f = inter.interp1d(b_wl, b_flux)
r_f = inter.interp1d(r_wl, r_flux)

# now we can create new x and y vectors for both parts, using the interpolation.
# this way we can make sure everything is consistent
b_wl = numpy.arange(ceil(b_wl[0]), b_wl[len(b_wl) - 1], 1)
r_wl = numpy.arange(ceil(r_wl[0]), r_wl[len(r_wl) - 1], 1)
b_flux = b_f(b_wl)
r_flux = r_f(r_wl)

# find out what value is the first one in the red x vector (wavelength)
# and what value is the last one of the blue x vector
# these are the limits of the overlap
first_r = r_wl[0]
last_b = b_wl[len(b_wl)-1]

# get what the limits are in terms of both parts' indices
for i in range(len(b_wl) - 1):
    if b_wl[i] == first_r:
        first_b_i = i
        break

for i in range(len(r_wl) - 1):
    if r_wl[i] == last_b:
        last_r_i = i
        break

# create the unified overlap part
y_over = numpy.zeros(last_r_i + 1)
for i in range(last_r_i + 1):
    y_over[i] = numpy.mean([b_flux[first_b_i], r_flux[i]])

# create the unified vectors
x_con = numpy.arange(min(b_wl), max(r_wl) + 1)
y_con = numpy.hstack((b_flux[:first_b_i], y_over))
y_con = numpy.hstack((y_con, r_flux[last_r_i + 1:]))

# now we plot
# this is the original figure, before the unification and averaging
plt.figure(1)
plt.plot(b_wl, b_flux, color='blue', linewidth=0.8)
plt.plot(r_wl, r_flux, color='red', linewidth=0.8)
# this plot is after the unification averaging
plt.figure(2)
plt.plot(x_con, y_con, linewidth=0.8)
plt.show()
