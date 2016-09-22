from full_func import full
import matplotlib.pyplot as plt

x_con, y_con = full()

z = 0.133

for i in range(len(x_con)):
    x_con[i] = x_con[i]/(1+z)

plt.plot(x_con, y_con)
plt.show()



