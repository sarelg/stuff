import matplotlib.pyplot as plt
import csv
from scipy.optimize import curve_fit
import numpy as np
from seeing_bins import const_width_bins

area = []
z = []
see = []
with open('/Users/sarelg/gastro/sdss/no_smooth/excels/area_under_sub+seeing50.csv', 'r') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        try:
            area.append(float(row[1]))
            z.append(float(row[3]))
            see.append(float(row[2]))
        except Exception:
            continue

plt.title('Area(Seeing50)')
plt.xlabel('Seeing50 Difference')
plt.ylabel('Area Under Subtraction')
plt.plot(see, area, '.')

x, y, sigma = const_width_bins(see, area)

x = x[1:]
y = y[1:]
sigma = sigma[1:]

def func(x, a, b):
    return a*x + b

x0 = [0, 0]
print(curve_fit(func, x, y, x0, sigma))

plt.show()

