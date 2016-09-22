from EW_lines import continuum
import astropy.modeling as mod
import numpy as np
import scipy.integrate as int
from diff_expo_plot import cor_exp
from matplotlib import pyplot as plt

data = cor_exp(490,51929,359)
x = data[6][0]
y = data[6][1]

# subtract the contiuum
y = continuum(x, y)

# isolate the OII line
for i in range(len(x)):
    if x[i] >= (3727 - 30):
        xfi = i
        break

for i in range(len(x)):
    if x[i] >= (3727 + 30):
        xff = i
        break

x1 = np.zeros(abs(xff - xfi))
y1 = np.zeros(abs(xff - xfi))

for i in range(len(x1)):
    x1[i] = x[xfi + i]
    y1[i] = y[xfi + i]

# define the gaussian for the fit
def cus_gauss(x, amplitude=1., mean=0., stddev=1.):
    return 1 + amplitude * np.exp(-((x-mean) ** 2)/(2 * (stddev ** 2)))
cus_mod = mod.models.custom_model(cus_gauss)

# perform the fit
g_init = cus_mod(2, 3727, 1)
fit_g = mod.fitting.LevMarLSQFitter()
g = fit_g(g_init, x1, y1)
y2 = g(x1)

# calcualte the equivalent width
def integrand(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x-mean) ** 2)/(2 * (stddev ** 2)))
xfit = np.arange(0., 10000., 1.)
yfit = integrand(xfit, g.amplitude, g.mean, g.stddev)
equwid = (int.simps(yfit))

plt.plot(x1, y1)
plt.plot(x1, y2)
plt.show()

