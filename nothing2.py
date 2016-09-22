# this is an experimental use of the sdss pixel masks
import csv
import numpy as np
import pickle
import matplotlib.pyplot as plt

f = csv.reader(open('./cluster/no_smooth/oiii_fit_num.csv'))

list = []
for row in f:
    try:
        if float(row[19]) > 1.5:
            list.append([row[0], float(row[19]), float(row[20])])
    except Exception:
        continue

list.sort(key=lambda list1: list1[1], reverse=True)

# datalist = np.zeros(len(list))
# for i in range(len(list)):
#     p = list[i][0]
#     data = pickle.load(open('/Users/sarelg/gastro/sdss/no_smooth/after_division/%s' % p, 'rb'))
for i in range(len(list)):
    p = list[i][0]
    z = list[i][2]
    data = pickle.load(open('/Users/sarelg/gastro/sdss/no_smooth/after_division/%s' % p, 'rb'))
    plt.figure()
    for j in range(len(data)):
        plt.plot(data[j][0], data[j][1])
        plt.title('%s, z = %s' % (p, z))

plt.show()