from diff_expo_plot import cor_exp
from EW_lines import oii, sii
import numpy as np

# data = cor_exp(491, 51942, 1)
data = cor_exp('spec-0491-51942-0001.fits')

ewo = np.zeros(len(data))
ews1 = np.zeros(len(data))
ews2 = np.zeros(len(data))
ampo = np.zeros(len(data))
amps1 = np.zeros(len(data))
amps2 = np.zeros(len(data))

for i in range(len(data)):
    x, y = data[i]
    ewo[i], ampo[i] = oii(x, y)
    ews1[i], ews2[i], amps1[i], amps2[i] = sii(x, y)

ampo_avg = np.mean(ampo)
amps1_avg = np.mean(amps1)
amps2_avg = np.mean(amps2)

amp = (ampo_avg, amps1_avg, amps2_avg)

stddev = [0]*3
stddev[0] = np.std(ewo)
stddev[1] = np.std(ews1)
stddev[2] = np.std(ews2)

print(np.mean(ewo), np.mean(ews1), np.mean(ews2))
print(stddev)

