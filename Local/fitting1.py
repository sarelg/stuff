from diff_expo_plot import cor_exp
import astropy.modeling as mod
import matplotlib.pyplot as plt

g1 = mod.models.Gaussian1D(2, 3728, 7)
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

# import the data
data = cor_exp(491, 51942, 1)[0]

# create the continuum fit
g_init = mod.models.PowerLaw1D(20, 3000, 0.5)
fit_g = mod.fitting.LevMarLSQFitter()
g = fit_g(g_init, data[0], data[1])

# subtract the continuum from the data
for i in range(len(data[0])):
    data[1][i] = data[1][i]/g(data[0][i])

for i in range(len(data[0])):
    data[1][i] = data[1][i] - 1

# fit the gaussians
g_g = fit_g(g_gauss, data[0], data[1])

plt.plot(data[0], data[1], 'r', lw=1, label='Data', drawstyle='steps-mid')
plt.plot(data[0], g_g(data[0]), label='Fit')
plt.legend()
plt.show()
