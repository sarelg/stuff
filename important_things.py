import numpy as np
import matplotlib.pyplot as plt
from var_dev_plot import plot_var
import pickle
import csv
import pyfits as pf
from full_func import full
from diff_expo_plot import cor_exp

# filename = 'spec-1604-53078-0013.fits.p'


# data = plot_var(filename, none = True)
# data1 = pickle.load(open('/Users/sarelg/gastro/sdss/no_smooth/none_trial/sub_exposures/%s' % filename, 'rb'))
#
# for i in range(len(data1)):
#     plt.plot(data1[i][0], data1[i][1])
#
# plt.xlim([4950, 5060])
# plt.figure()
#
# sorti = []
# for i in range(len(data)):
#     sorti.append(max(data[i]))
#
# # find out which exposure is the min and which is the max
# min1, max1 = np.argmin(sorti), np.argmax(sorti)
#
# # make the subtracted vector
# vec = data[max1] - data[min1]
# vec = vec[~np.isnan(vec)]
# area = np.trapz(vec)
# med = np.median([data[max1], data[min1]], axis=0)
# med = med[~np.isnan(med)]
# print(area/np.trapz(med))
# plt.plot(med, 'o')
#
# plt.show()

# reader = csv.reader(open('/Users/sarelg/gastro/sdss/no_smooth/area_under_subtraction.csv', 'r'))
#
# reader.__next__()
#
# area = []
# z = []
# for row in reader:
#     area.append(row[1])
#     z.append(row[2])
#
# plt.plot(z, area, '.')
#
# plt.show()


file_list = []
with open('/Users/sarelg/gastro/sdss/no_smooth/excels/1000.csv', 'r') as csvfile:
    f = csv.reader(csvfile)
    f.__next__()
    for row in f:
        file_list.append(row[0])

files = []
for i in range(20):
    files.append(file_list[i])

for i in range(len(files)):

    # try:
        plt.figure()
        data1 = pickle.load(open('/Users/sarelg/gastro/sdss/no_smooth/none_trial/sub_exposures/%s' % files[i], 'rb'))

        for j in range(len(data1)):
            plt.plot(data1[j][0], data1[j][1])

        plt.title(files[i])
        plt.xlim([4950, 5060])
    # except Exception:
    #     continue

plt.show()