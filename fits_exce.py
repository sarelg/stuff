import pyfits as pf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

path_fits = r'C:\Users\Sarel\Desktop\physics\Research\NLR\fits\spec-0491-51942-0001.fits'


def data_lists(path):
    global b_data, r_data, b_flux, r_flux, b_wl, r_wl
    b_data = [0]*9
    r_data = [0]*9
    b_flux = [0]*9
    r_flux = [0]*9
    b_wl = [0]*9
    r_wl = [0]*9
    for i in range(9):
        b_data[i] = pf.getdata(path, i+4)
        r_data[i] = pf.getdata(path, i+13)

        b_flux[i] = b_data[i]['flux']
        r_flux[i] = r_data[i]['flux']

        b_wl[i] = 10**b_data[i]['loglam']
        r_wl[i] = 10**r_data[i]['loglam']


def time_diff(path, first_ex, second_ex):
    first_hdr = pf.getheader(path, first_ex+4)
    second_hdr = pf.getheader(path, second_ex+4)
    diff = abs(first_hdr.cards['tai'].value-second_hdr.cards['tai'].value)
    diff = round(diff/60)
    return diff

data_lists(path_fits)


def plot_spec(*args):
    for i in args:
        plt.plot(b_wl[i], b_flux[i], linewidth=0.8)
        plt.plot(r_wl[i], r_flux[i], linewidth=0.8)
    if 'average' in args:
        plt.plot(10**pf.getdata(path_fits, 1)['loglam'], pf.getdata(path_fits, 1)['flux'], color='black', linewidth=0.9)
    plt.show()

plot_spec(0, 1)

# plt.plot(b_wl[0], b_flux[0], linewidth=0.8)
# plt.plot(r_wl[0], r_flux[0], color='blue', linewidth=0.8)
# plt.plot(b_wl[1], b_flux[1], color='red', linewidth=0.8)
# plt.plot(r_wl[1], r_flux[1], color='red', linewidth=0.8)
# plt.plot(10**pf.getdata(path_fits, 1)['loglam'], pf.getdata(path_fits, 1)['flux'], color='black', linewidth=0.9)
# # plt.xlim(5400, 5600)
# # plt.ylim(20, 70)
# blue_leg = mpatch.Patch(color='blue', label='First Exposure')
# black_leg = mpatch.Patch(color='black', label='Average Flux')
# red_leg = mpatch.Patch(color='red', label=str(time_diff(path_fits, 0, 1)) + ' minutes')
# plt.legend(handles=[blue_leg, red_leg, black_leg])
# plt.show()




# b_1_data = pf.getdata(path, 4)
# b_2_data = pf.getdata(path, 5)
# r_1_data = pf.getdata(path, 14)
#
# flux_b_1 = b_1_data['flux']
# flux_b_2 = b_2_data['flux']
# flux_r_1 = r_1_data['flux']
#
# wl_b_1 = 10**b_1_data['loglam']
# wl_b_2 = 10**b_2_data['loglam']
# wl_r_1 = 10**r_1_data['loglam']
#
# plt.plot(wl_b_1, flux_b_1)
# plt.plot(wl_r_1, flux_r_1, 'blue')
# plt.show()


# diff = abs(first_b_hdr.cards['tai'].value - second_b_hdr.cards['tai'].value)
# diff = round(diff/60)
#
# # print(hdulist[4].header.cards['tai'].value)
#
# blue_leg = mpatch.Patch(color='blue', label='time = 0')
# red_leg = mpatch.Patch(color='red', label=r'time = %s minutes' % (diff))
#
# plt.figure(1)
# plt.plot(first_b_data, linewidth=0.5, color='blue')
# plt.plot(second_b_data, linewidth=0.5, color='red')
# plt. title('First Two Blue Exposures')
# plt.ylabel('Flux')
# plt.xlabel('Wavelength')
# plt.legend(handles=[blue_leg, red_leg])
# plt.show()

