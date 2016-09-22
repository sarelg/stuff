# this script will take a list from a csv of the brightest objects and plot them on a std, z plot
import csv

# get the files from the source and match the names with the output file
source = csv.reader(open('./brightest600.csv', 'r'))
c = open('./cluster/oiii_num.csv')
current = csv.reader(c)
output = csv.writer(open('./cluster/brightest_res.csv', 'w'))
for row in source:
    plate = row[0]
    plate = plate.zfill(4)
    mjd = row[1]
    fiber = row[2]
    fiber = fiber.zfill(4)
    for row2 in current:
        if row2[0] == 'spec-%s-%s-%s.fits.p' % (plate, mjd, fiber):
            output.writerow([row2[0], row2[19], row2[20]])
            c.seek(0)
            break
        elif row2[0] == 'spec-2035-53436-0385.fits.p':
            c.seek(0)
            break