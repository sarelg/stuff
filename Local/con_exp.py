import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as inter

x1 = np.array([1, 2, 3, 4, 5])
x2 = np.array([4, 6, 8, 10])

y1 = np.array([34, 56, 23, 45, 65])
y2 = np.array([45, 65, 12, 56])

f1 = inter.interp1d(x1, y1)
f2 = inter.interp1d(x2, y2)
x1 = np.arange(min(x1), max(x1) + 1, 1)
x2 = np.arange(min(x2), max(x2) + 1, 1)
y1 = f1(x1)
y2 = f2(x2)
first2 = x2[0]
last1 = x1[len(x1) - 1]

print(x1, x2)

for i in range(len(x1) - 1):
    if x1[i] == first2:
        first1i = i
        break

for i in range(len(x2) - 1):
    if x2[i] == last1:
        last2i = i
        break

y_over = np.zeros(last2i + 1)
for i in range(last2i + 1):
    y_over[i] = np.mean([y1[first1i], y2[i]])

# create the unified vectors
x_con = np.arange(min(x1), max(x2) + 1)
y_con = np.hstack((y1[:first1i], y_over))
y_con = np.hstack((y_con, y2[last2i + 1:]))

print(x1,x2)
print(y1, y2, y_over)
print(x_con, y_con)

# now we plot
# this is the original figure, before the unification and averaging
plt.figure(1)
plt.plot(x1, y1, color='blue', linewidth=0.8)
plt.plot(x2, y2, color='blue', linewidth=0.8)
# this plot is after the unification averaging
plt.figure(2)
plt.plot(x_con, y_con, linewidth=0.8)
plt.show()
