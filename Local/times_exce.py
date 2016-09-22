from os import listdir


def check_time(file_name):
    import pyfits as pf

    path = './fits/%s' % file_name

    nexp = int(pf.getheader(path, 0)['nexp']/2) - 1

    tup = [0]*nexp
    for i in range(nexp):
        tup[i] = (pf.getheader(path, i + 4)['tai-beg'],
                  pf.getheader(path, i + 4)['extname'])

    tup_new = sorted(tup, key=lambda t: t[0])

    count = 0
    for i in range(len(tup)):
        if tup[i] != tup_new[i]:
            print('mismatch at number %d' % i)
            count += 1

    if count == 0:
        print('no problems')

list1 = listdir('./fits/')

for j in range(1, len(list1)):
    check_time(list1[j])

