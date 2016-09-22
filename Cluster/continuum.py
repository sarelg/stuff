"""This function fits the contiuum of a spectrum and returns a y-vector
normalised by it"""


def continuum(x, y):
    import astropy.modeling as mod
    import numpy as np

    xf1 = np.zeros(6300-5150)
    yf1 = np.zeros(6300-5150)
    xf2 = np.zeros(8000-7000)
    yf2 = np.zeros(8000-7000)

    for i in range(len(x)):
        if x[i] >= 5150:
            x1i = i
            break

    for i in range(6300-5150):
        xf1[i] = x[x1i + i]
        yf1[i] = y[x1i + i]

    for i in range(8000-7000):
        xf2[i] = x[x1i + 1850 + i]
        yf2[i] = y[x1i + 1850 + i]

    # make a single vector out of the line-free areas
    xf = np.hstack((xf1, xf2))
    yf = np.hstack((yf1, yf2))

    # fit a power law
    g_init = mod.models.PowerLaw1D(20, 5150, 0.5)
    fit_g = mod.fitting.LevMarLSQFitter()
    g = fit_g(g_init, xf1, yf1)

    # suctract the continuum
    for i in range(len(x)):
        y[i] = y[i]/g(x[i])

    return y