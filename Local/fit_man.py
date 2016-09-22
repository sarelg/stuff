"""This is the attempt to manually create a continuum fit without the areas
 where the lines are, and create equivalent widths for each gaussian"""

from diff_expo_plot import cor_exp
import astropy.modeling as mod
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as int

def cus_gauss(x, amplitude = 1., mean = 0., stddev = 1.):
    return 1 + amplitude * np.exp(-((x-mean) ** 2)/(2 * (stddev ** 2)))
cus_mod = mod.models.custom_model(cus_gauss)

# create gaussians
g1 = cus_mod(2, 3728, 7)
g2 = mod.models.Gaussian1D(2, 4861, 2)
g3 = mod.models.Gaussian1D(2, 4861, 7)
g4 = mod.models.Gaussian1D(2, 4960, 5)
g5 = mod.models.Gaussian1D(3, 5007, 8)
g6 = mod.models.Gaussian1D(3, 6550, 5)
g7 = mod.models.Gaussian1D(6, 6563, 10)
g8 = mod.models.Gaussian1D(3.5, 6585, 5)
g9 = mod.models.Gaussian1D(2, 6718, 5)
g10 = mod.models.Gaussian1D(1.5, 6735, 3)

g_gauss = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9 + g10
# import the data we are going to use and chop it to line-free areas
data = cor_exp(491, 51942, 1)[0]

xf1 = np.zeros(6300-5150)
yf1 = np.zeros(6300-5150)
xf2 = np.zeros(8000-7000)
yf2 = np.zeros(8000-7000)

for i in range(len(data[0])):
    if data[0][i] >= 5150:
        x1i = i
        break

for i in range(6300-5150):
    xf1[i] = data[0][x1i + i]
    yf1[i] = data[1][x1i + i]

for i in range(8000-7000):
    xf2[i] = data[0][x1i + 1850 + i]
    yf2[i] = data[1][x1i + 1850 + i]
# make a single vector out of the line-free areas
xf = np.hstack((xf1, xf2))
yf = np.hstack((yf1, yf2))
# fit a power law
g_init = mod.models.PowerLaw1D(20, 5150, 0.5)
fit_g = mod.fitting.LevMarLSQFitter()
g = fit_g(g_init, xf1, yf1)

# subtract the continuum from the data
for i in range(len(data[0])):
    data[1][i] = data[1][i]/g(data[0][i])

# fit the gaussians
g_g = fit_g(g_gauss, data[0], data[1])

# put variables into array
par = [0]*10
for i in range(len(par)):
    par[i] = g_g[i].amplitude, g_g[i].mean, g_g[i].stddev


def integrand(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x-mean) ** 2)/(2 * (stddev ** 2)))

x = np.arange(0., 10000., 1)
ew = [0]*10
for i in range(len(par)):
    amplitude = par[i][0]/1.0
    mean = par[i][1]/1.0
    stddev = par[i][2]/1.0
    y = integrand(x, amplitude, mean, stddev)
    ew[i] = (int.simps(y))

print(ew)

plt.plot(data[0], data[1], label='Data')
plt.plot(data[0], g_g(data[0]), 'r', label='Fit')
plt.legend()
plt.show()
