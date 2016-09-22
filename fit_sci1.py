"""This is an another attempt to fit the spectrum using
the scipy.optimize function"""

from diff_expo_plot import cor_exp
import matplotlib.pyplot as plt
from scipy import optimize as opt
import numpy as np

tup = (0, 1, 977, 3, 3, 1035, 3, 10, 1215, 3, 50, 1215, 1 ,3, 1240, 3,
        1.3, 1400, 3, 6, 1549, 3, 12, 1549, 1, 3, 1909, 3, 5, 1909, 1,
        8, 2600, 3, 3, 2798, 3, 2, 2798, 1, 1, 3426, 1, 3, 3727, 1,
        1.5, 3869, 1, 1, 4861, 3, 1, 4861, 1, 12, 5007, 1, 2, 5000, 3,
        1, 6300, 1, 5, 6563, 3, 3, 6563, 1, 3, 6583, 1, 2, 6716, 1,
        2, 6731, 1)


def func(x, tup, b, c, d):
    return (b * ((x/c) ** -d)) * \
    (tup[1] * np.exp(-((x - tup[2]) ** 2) / (2 * (tup[3] ** 2))) +
     tup[4] * np.exp(-((x - tup[5]) ** 2) / (2 * (tup[6] ** 2))) +
     tup[7] * np.exp(-((x - tup[8]) ** 2) / (2 * (tup[9] ** 2))) +
     tup[10] * np.exp(-((x - tup[11]) ** 2) / (2 * (tup[12] ** 2))) +
     tup[13] * np.exp(-((x - tup[14]) ** 2) / (2 * (tup[15] ** 2))) +
     tup[16] * np.exp(-((x - tup[17]) ** 2) / (2 * (tup[18] ** 2))) +
     tup[19] * np.exp(-((x - tup[20]) ** 2) / (2 * (tup[21] ** 2))) +
     tup[22] * np.exp(-((x - tup[23]) ** 2) / (2 * (tup[24] ** 2))) +
     tup[25] * np.exp(-((x - tup[26]) ** 2) / (2 * (tup[27] ** 2))) +
     tup[28] * np.exp(-((x - tup[29]) ** 2) / (2 * (tup[30] ** 2))) +
     tup[31] * np.exp(-((x - tup[32]) ** 2) / (2 * (tup[33] ** 2))) +
     tup[34] * np.exp(-((x - tup[35]) ** 2) / (2 * (tup[36] ** 2))) +
     tup[37] * np.exp(-((x - tup[38]) ** 2) / (2 * (tup[39] ** 2))) +
     tup[40] * np.exp(-((x - tup[41]) ** 2) / (2 * (tup[42] ** 2))) +
     tup[43] * np.exp(-((x - tup[44]) ** 2) / (2 * (tup[45] ** 2))) +
     tup[46] * np.exp(-((x - tup[47]) ** 2) / (2 * (tup[48] ** 2))) +
     tup[49] * np.exp(-((x - tup[50]) ** 2) / (2 * (tup[51] ** 2))) +
     tup[52] * np.exp(-((x - tup[53]) ** 2) / (2 * (tup[54] ** 2))) +
     tup[55] * np.exp(-((x - tup[56]) ** 2) / (2 * (tup[57] ** 2))) +
     tup[58] * np.exp(-((x - tup[59]) ** 2) / (2 * (tup[60] ** 2))) +
     tup[61] * np.exp(-((x - tup[62]) ** 2) / (2 * (tup[63] ** 2))) +
     tup[64] * np.exp(-((x - tup[65]) ** 2) / (2 * (tup[66] ** 2))) +
     tup[67] * np.exp(-((x - tup[68]) ** 2) / (2 * (tup[69] ** 2))) +
     tup[70] * np.exp(-((x - tup[71]) ** 2) / (2 * (tup[72] ** 2))) +
     tup[73] * np.exp(-((x - tup[74]) ** 2) / (2 * (tup[75] ** 2))) +
     tup[76] * np.exp(-((x - tup[77]) ** 2) / (2 * (tup[78] ** 2))) + 1)

data = cor_exp(491, 51942, 1)[0]

x = data[0]
y = data[1]

initial = (tup, 20, 3000, 0.5)

def error(x, tup, b, c, d):
    return y - func(x, tup, b, c, d)

g = opt.leastsq(error(x, tup, 20, 3000, 0.5), initial)

plt.plot(x, y, 'b')
plt.plot(x, func(x, tup, 20, 3000, 0.5), 'r')
plt.show()