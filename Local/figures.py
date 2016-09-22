from diff_expo_plot import draw
import matplotlib.pyplot as plt

plt.figure(1)
plt.title('1018-52672-0359 - high std to 1/sn')
draw(1018,52672,359)

plt.figure(2)
plt.title('5942-56210-0308 - high std to 1/sn')
draw(5942,56210,308)

plt.figure(3)
plt.title('2207-53558-227 - high std to 1/sn')
draw(2207,53558,227)

plt.figure(4)
plt.title('0266-51630-0227 - low std to 1/sn')
draw(266,51630,227)

plt.figure(5)
plt.title('4776-55652-0334 - low std to 1/sn')
draw(4776,55652,334)

plt.show()