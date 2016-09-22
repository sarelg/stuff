# from full_func import full
from scipy.signal import savgol_filter, medfilt
import matplotlib.pyplot as plt
import pyfits as pf

b_flux = pf.getdata('./fits/spec-0571-52286-0533.fits', 4)['flux']
r_flux = pf.getdata('./fits/spec-0571-52286-0533.fits', 9)['flux']
b_wl = 10 ** pf.getdata('./fits/spec-0571-52286-0533.fits', 4)['loglam']
r_wl = 10 ** pf.getdata('./fits/spec-0571-52286-0533.fits', 9)['loglam']

b_flux = medfilt(b_flux, 11)
b_flux = savgol_filter(b_flux, 49, 11)
r_flux = medfilt(r_flux, 11)
r_flux = savgol_filter(r_flux, 49, 11)

plt.plot(b_wl, b_flux, r_wl, r_flux)
plt.show()
