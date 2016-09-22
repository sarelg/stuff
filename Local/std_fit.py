# this script will create a line for the typical standard deviation as a function of redshift
# using the EW calculated numerically
# [add calculation for fitted EW]
import csv
import numpy as np
from matplotlib import pyplot as plt
from astropy import modeling as mod

# read the csv file and skip the header line
f = csv.reader(open('./cluster/no_smooth/oiii_fit_num.csv'))
f2 = csv.reader(open('./cluster/no_smooth/oiii_fit_num.csv'))
# f3 = csv.reader(open('./cluster/oiii_fit_num2.csv'))
data = []
data2 = []
# data3 = []
f.__next__()
f2.__next__()
# f3.__next__()

# put the std and z in a list of lists
for row in f:
    try:
        med_list = []
        for i in range(len(row)):
            if len(row[i+1]) == 0:
                break
            else:
                med_list.append(float(row[i+1]))
        median = np.median(med_list)
        dist_list = np.absolute(median - med_list)
        mad = np.median(dist_list)
        data.append([float(row[19]),float(row[20]),mad/median])
    except Exception:
        data.append([0, float(row[20]), 0])
for row2 in f2:
    try:
        data2.append([float(row2[19]),float(row2[20])])
    except Exception:
        data2.append([0, float(row2[20])])


# for row3 in f3:
#     try:
#         data3.append([float(row3[19]),float(row3[20])])
#     except Exception:
#         data3.append([0, float(row3[20])])

# sort by z
data.sort(key=lambda list1: list1[1])
data2.sort(key=lambda list2: list2[1])
# data3.sort(key=lambda list2: list2[1])

# divide back to two lists
std1 = []
z1 = []
mad1 = []
std2 = []
z2 = []
# std3 = []
# z3 = []
for i in range(len(data)):
    std1.append(data[i][0])
    z1.append(data[i][1])
    mad1.append(data[i][2])
for i in range(len(data2)):
    std2.append(data2[i][0])
    z2.append(data2[i][1])
    # std3.append(data3[i][0])
    # z3.append(data3[i][1])

# get the average of ten objects
avg_mad1 = []
avg_z1 = []
x = 100
for i in range(len(data)):
    if i%x == 0:
        avg_mad_loc1= np.average(mad1[i:i+x])
        avg_mad1.append(avg_mad_loc1)
        avg_z_loc1 = np.average(z1[i:i+x])
        avg_z1.append(avg_z_loc1)
    elif i == 5689:
        break

avg_std2 = []
avg_z2 = []
x = 100
for i in range(len(data2)):
    if i % x == 0:
        avg_std_loc2 = np.average(std2[i:i + x])
        avg_std2.append(avg_std_loc2)
        avg_z_loc2 = np.average(z2[i:i + x])
        avg_z2.append(avg_z_loc2)
    elif i == 5689:
        break
#
# avg_std3 = []
# avg_z3 = []
# x = 100
# for i in range(len(data)):
#     if i % x == 0:
#         avg_std_loc3 = np.average(std3[i:i + x])
#         avg_std3.append(avg_std_loc3)
#         avg_z_loc3 = np.average(z3[i:i + x])
#         avg_z3.append(avg_z_loc3)
#     elif i == 5689:
#         break

# fit a function
g_init1 = mod.models.LogParabola1D(0.018, 0.1, -0.5, 10)
fit_g1 = mod.fitting.LevMarLSQFitter()
g1 = fit_g1(g_init1, avg_z1, avg_mad1)

g_init2 = mod.models.LogParabola1D(0.018, 0.1, -0.5, 10)
fit_g2 = mod.fitting.LevMarLSQFitter()
g2 = fit_g2(g_init2, avg_z2, avg_std2)
#
# g_init3 = mod.models.LogParabola1D(0.018, 0.1, -0.5, 10)
# fit_g3 = mod.fitting.LevMarLSQFitter()
# g3 = fit_g3(g_init3, avg_z3, avg_std3)

# print(g.amplitude, g.x_0, g.alpha, g.beta)
# plot
line1, = plt.plot(avg_z1, avg_mad1, '.')
plt.plot(avg_z1, g1(avg_z1), 'g')
line2, = plt.plot(avg_z2, avg_std2, '*')
plt.plot(avg_z2, g2(avg_z2), 'b')
# line3, = plt.plot(avg_z3, avg_std3, 'o')
# plt.plot(avg_z3, g3(avg_z3), 'black')
plt.xlabel('Z')
plt.ylabel('Average STD/EW')
# plt.legend((line1, line2, line3), ('Simple EW', 'Fixed Line Fit EW', 'Free Line Fit EW'), loc=2, numpoints=1)
plt.show()
