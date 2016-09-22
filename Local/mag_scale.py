# this script will show the std/avg and mad/median as a function of z graphs
# for objects of the same EW scale
import csv
import numpy as np
import pyfits as pf
from os import listdir
from multiprocessing import Pool
import matplotlib.pyplot as plt
import pickle

# f = open('./cluster/no_smooth/flux.csv', 'w')
# writer = csv.writer(f)
# fits = listdir('/Users/sarelg/gastro/sdss/files/')
# del fits[0]
# del fits[0]


# def fluxlist(fits_file):
#     # try:
#         flux_list = ([fits_file, pf.getdata('/Users/sarelg/gastro/sdss/files/%s' % fits_file
#                                                 , 2)['spectroflux'][0][1]])
#         return flux_list
#     # except Exception:
#
# pool = Pool(processes=None)
# for result in pool.map(fluxlist, fits):
#     writer.writerow(result)
#
# print('All done!')

# f_z = open('./cluster/no_smooth/z_sdss_no_smooth.csv')
# f_flux = open('./cluster/no_smooth/flux.csv')
# f_out = open('./cluster/no_smooth/out.csv')
# reader_z = csv.reader(f_z)
# reader_flux = csv.reader(f_flux)
# reader_out = csv.reader(f_out)
# reader_z.__next__()
#
# # def match(reader, writer):
# for row in reader_z:
#     a = row[0].replace('.p', '')
#     for row2 in reader_flux:
#         if a == row2[0]:
#             writer_out.writerow([a, row2[1], row[1]])
#             f_flux.seek(0)
#             break
#         elif row2[0] == 'spec-2035-53436-0385.fits':
#             f_flux.seek(0)
#             break
#
# f_z.close()
# f_flux.close()
# f_out.close()

f_flux = open('./cluster/no_smooth/flux.csv')
f_oiii = open('./cluster/no_smooth/oiii_num.csv')
f_out = open('./cluster/no_smooth/mag_scale.csv', 'w')
f_out2 = open('./cluster/no_smooth/mag_scale.csv')
reader_flux = csv.reader(f_flux)
reader_oiii = csv.reader(f_oiii)
writer_out = csv.writer(f_out)
reader_oiii.__next__()
reader_out = csv.reader(f_out2)

for row in reader_oiii:
    # a = row[0].replace('.p', '')
    for row2 in reader_flux:
        if 20 < float(row2[1]) < 40:
            writer_out.writerow([row[0], row2[1], row[19], row[20]])
            break
        else:
            break

f_out.close()

std = []
z = []
for row in reader_out:
    try:
        std.append(float(row[2]))
        z.append(float(row[3]))
    except Exception:
        std.append(0)
        z.append(float(row[3]))


f_flux.close()
f_oiii.close()
f_out2.close()

data = pickle.load(open('/Users/sarelg/gastro/sdss/no_smooth/after_division/spec-1013-52707-0484.fits.p', 'rb'))
plt.figure()
for j in range(len(data)):
    plt.step(data[j][0], data[j][1])
    plt.title('spec-1013-52707-0484.fits')

plt.figure()
plt.plot(z, std, '.')
plt.show()






