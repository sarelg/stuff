"""This is an attempt to fit the spectrum using the scipy.optimize function"""

from diff_expo_plot import cor_exp
import matplotlib.pyplot as plt
from scipy import optimize as opt
import numpy as np

# first we define parameters for each of the lines
para = {'CIII977':(1, 977, 3), 'OVI1035':(3, 1035, 3), 'Lalphab':(10, 1215, 3),
        'Lalphan':(50, 1215, 1), 'NV1240':(3, 1240, 3),
        'SiIV,OIV]1400':(1.3, 1400, 3), 'CIV1549b':(6, 1549, 3),
        'CIV1549n':(12, 1549, 1), 'CIII]1909b':(3, 1909, 3),
        'CIII]1909n':(5, 1909, 1), 'FeII1':(8, 2600, 3), 'MgII2798b':(3, 2798, 3),
        'MgII2798n':(2, 2798, 1), '[NeV]3426':(1, 3426, 1),
        'OII]lambda3727':(3, 3727, 1), '[NeIII]3869':(1.5, 3869, 1),
        'Hbetab':(1, 4861, 3), 'Hbetan':(1, 4861, 1), '[OIII]5007':(12, 5007, 1),
        'FeII2':(2, 5000, 3), '[OI]6300':(1, 6300, 1),
        'Halphab':(5, 6563, 3), 'Halphan':(3, 6563, 1),
        '[NII]6583':(3, 6583, 1), '[SII]6716':(2, 6716, 1),
        '[SII]6731':(2, 6731, 1)}

# import data
data = cor_exp(491, 51942, 1)[0]

x = data[0]
y = data[1]


# now define the function we are going to use
def funct(x, para):
    final = 0
    for i in para:
        def func(x, para):
            para1, para2, para3 = para[i]
            return (para1 *
                    np.exp(-((x - para2) ** 2) /
                        (2 * (para3 ** 2))))
        final += func(x, para)

    final = (20 * ((x/3000) ** -0.5)) * (final + 1)
    return final


def error_func(x, para):
    return funct(x, para) - y

lst = []
for i in para:
    lst.append(para[i])

g = opt.leastsq(error_func(x, para), lst)

print(g)
plt.plot(x, y, 'b')
plt.plot(x, func(x, para), 'r')
plt.show()