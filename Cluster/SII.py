"""this function calcualtes the equivalent width of the SII6716, SII6731
 lines"""


def sii(x, y):
    import astropy.modeling as mod
    import numpy as np
    import scipy.integrate as int
    from continuum import continuum

    # subtract the contiuum
    y = continuum(x, y)

    # isolate the SII lines
    x1 = np.zeros(75)
    y1 = np.zeros(75)

    for i in range(len(x)):
        if x[i] >= (6716 - 30):
            xfi = i
            break

    for i in range(75):
        x1[i] = x[xfi + i]
        y1[i] = y[xfi + i]

    # define the gaussian for the fit
    def cus_gauss(x, amplitude=1., mean=0., stddev=1.):
        return 1 + amplitude * np.exp(-((x-mean) ** 2)/(2 * (stddev ** 2)))
    cus_mod = mod.models.custom_model(cus_gauss)

    # perform the fit
    g1 = cus_mod(1, 6716, 1)
    g2 = mod.models.Gaussian1D(1, 6731, 1)
    g_init = g1 + g2
    fit_g = mod.fitting.LevMarLSQFitter()
    g = fit_g(g_init, x1, y1)

    # calcualte the equivalent width
    def integrand(x, amplitude, mean, stddev):
        return amplitude * np.exp(-((x-mean) ** 2)/(2 * (stddev ** 2)))
    xfit = np.arange(0., 10000., 1.)
    yfit = integrand(xfit, g.amplitude, g.mean, g.stddev)
    equwid = (int.simps(yfit))

    return equwid
