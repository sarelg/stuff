import matplotlib.pyplot as plt
import csv

reader = csv.reader(open('./cluster/no_smooth/dev_est.csv', 'r'))
reader.__next__()
line_frac = []
z = []
name = []
for row in reader:
    try:
        line_frac.append(float(row[3]))
        z.append(float(row[4]))
        name.append(row[0])
    except Exception:
        name.append(0)
        line_frac.append(0)
        z.append(0)

all = []
for i in range(len(name)):
    all.append([name[i], line_frac[i], z[i]])

all.sort(key=lambda list1: list1[1], reverse=True)
for i in range(10):
    print(all[i][0], all[i][1])


# m = max(line_frac)
# i = line_frac.index(m)
# print(name[i])

# plt.plot(z, line_frac, '.')
# plt.show()