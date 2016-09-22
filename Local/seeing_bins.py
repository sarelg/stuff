import matplotlib.pyplot as plt
import csv
from scipy import stats
import numpy as np


def const_width_bins(see, area, see_marked, area_marked):
    x = np.arange(-3, 3, 0.7)
    y_mean = []
    y_std = []
    y_med = []
    y_mad = []
    x_mean = []
    lastj = 0
    for i in range(len(x)):
        list1 = []
        list2 = []
        for j in range(len(area)):
            if see[lastj+j] == see[-1]:
                break
            elif see[lastj + j] <= x[i]:
                list1.append(area[lastj+j])
                list2.append(see[lastj+j])
            else:
                lastj = lastj + j
                break

        x_mean.append(np.mean(list2))
        y_mean.append(np.mean(list1))
        y_std.append(np.std(list1))
        y_med.append(np.median(list1))
        list2 = []
        for k in range(len(list1)):
            list2.append(abs(list1[k] - np.median(list1)))
        y_mad.append(np.median(list2))

    markleg, = plt.plot(see_marked, area_marked, 'D', color='cyan', zorder=12)
    mean = plt.errorbar(x, y_mean, yerr = y_std, zorder = 10, fmt = 'o-', color = 'red', lw = 1.5)
    median = plt.errorbar(x, y_med, yerr = y_mad, zorder = 11, fmt = 'o-', color = 'green', lw = 1.5)
    plt.legend([mean, median,], ['Mean', 'Median'], loc = 'lower right', numpoints = 1)
    plt.xlim(-2.5, 3)
    plt.ylim(-0.2, 0.3)


def const_num_bins(see, area):
    bins = 10
    x = int(len(see)/bins)
    datax = []
    datay = []
    datax_mean = []
    datay_mean = []
    datax_med = []
    datay_med = []
    for i in range(bins):
        datax.append(see[i*x:(i+1)*x])
        datay.append(area[i*x:(i+1)*x])

    datay_std = []
    datay_mad = []
    for i in range(len(datax)):
        datax_mean.append(np.mean(datax[i]))
        datay_std.append(np.std(datay[i]))
        datay_mean.append(np.mean(datay[i]))
        datax_med.append(np.median(datax[i]))
        datay_med.append(np.median(datay[i]))
        a = []
        for j in range(len(datay[i])):
            a.append(abs(np.median(datay[i]) - datay[i][j]))
        datay_mad.append(np.median(a))
    mean = plt.errorbar(datax_mean, datay_mean, yerr = datay_std, fmt  = 'o-', lw = 2, zorder=10, color='red')
    median = plt.errorbar(datax_med, datay_med, yerr=datay_mad, fmt='o-', lw=2, zorder=11, color='green')
    plt.legend([mean, median], ['Mean', 'Median'], numpoints=1)
    plt.xlim(-0.5, 0.7)
    plt.ylim(-0.2, 0.2)

if __name__ == '__main__':
    area = []
    z = []
    see = []
    marked = []
    with open('/Users/sarelg/gastro/sdss/no_smooth/excels/area_under_sub+seeing50_markedboth.csv', 'r') as csvfile:
        f = csv.reader(csvfile)
        for row in f:
            try:
                area.append(float(row[1]))
                z.append(float(row[3]))
                see.append(float(row[2]))
                marked.append(row[4])

            except Exception:
                continue

    # see_un = []
    # see_marked = []
    # area_un = []
    # area_marked = []
    # for i in range(len(see)):
    #     if marked[i] == 'TRUE':
    #         see_marked.append(see[i])
    #         area_marked.append(area[i])
    #     else:
    #         see_un.append(see[i])
    #         area_un.append(area[i])

    # a1 = []
    # a2 = []
    # a3 = []
    # b1 = []
    # b2 = []
    # b3 =[]
    # for i in range(len(see)):
    #     if z[i] <= 0.1:
    #         a1.append(see[i])
    #         a2.append(area[i])
    #         a3.append(marked[i])
    #     else:
    #         b1.append(see[i])
    #         b2.append(area[i])
    #         b3.append(marked[i])
    #
    # see_una = []
    # see_markeda = []
    # area_una = []
    # area_markeda = []
    # for i in range(len(a1)):
    #     if a3[i] == 'TRUE':
    #         see_markeda.append(a1[i])
    #         area_markeda.append(a2[i])
    #     else:
    #         see_una.append(a1[i])
    #         area_una.append(a2[i])
    #
    # const_width_bins(a1, a2, see_markeda, area_markeda)
    #
    # plt.plot(see_una, area_una, '.')
    #
    # see_unb = []
    # see_markedb = []
    # area_unb = []
    # area_markedb = []
    # for i in range(len(b1)):
    #     if b3[i] == 'TRUE':
    #         see_markedb.append(b1[i])
    #         area_markedb.append(b2[i])
    #     else:
    #         see_unb.append(b1[i])
    #         area_unb.append(b2[i])
    #
    # plt.figure()
    # const_width_bins(b1, b2, see_markedb, area_markedb)
    # plt.plot(see_unb, area_unb, '.')
    #
    #
    #
    # # const_width_bins(see, area, see_marked, area_marked)
    # # plt.plot(see_un, area_un, '.')
    # plt.show()
















    a1 = []
    a2 = []
    b1 = []
    b2 = []
    c1 = []
    c2 = []
    d1 = []
    d2 = []
    for i in range(len(z)):
        if z[i] <= 0.05:
            a1.append(see[i])
            a2.append(area[i])
        elif 0.05 < z[i] <= 0.1:
            b1.append(see[i])
            b2.append(area[i])
        elif 0.1 < z[i] <= 0.15:
            c1.append(see[i])
            c2.append(area[i])
        elif 0.15 < z[i] <= 0.2:
            d1.append(see[i])
            d2.append(area[i])

    plt.figure(1)
    plt.title('Area(Seeing50), z < 0.05')
    plt.xlabel('Seeing50 Difference')
    plt.ylabel('Area Under Subtraction')
    plt.plot(a1, a2, '.')
    const_num_bins(a1, a2)

    plt.figure(2)
    plt.title('Area(Seeing50), 0.05 < z < 0.1')
    plt.xlabel('Seeing50 Difference')
    plt.ylabel('Area Under Subtraction')
    plt.plot(b1, b2, '.')
    const_num_bins(b1, b2)

    plt.figure(3)
    plt.title('Area(Seeing50), 0.1 < z < 0.15')
    plt.xlabel('Seeing50 Difference')
    plt.ylabel('Area Under Subtraction')
    plt.plot(c1, c2, '.')
    const_num_bins(c1, c2)

    plt.figure(4)
    plt.title('Area(Seeing50), 0.15 < z < 0.2')
    plt.xlabel('Seeing50 Difference')
    plt.ylabel('Area Under Subtraction')
    plt.plot(d1, d2, '.')
    const_num_bins(d1, d2)
    plt.show()