#!/usr/bin/env python


import csv

ifile  = open('ESCBASGENARINADUGARTEC2.csv', "rb")
reader = csv.reader(ifile)
ofile  = open('prueba.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

for row in reader:
    print row
    #writer.writerow(row)

ifile.close()
ofile.close()