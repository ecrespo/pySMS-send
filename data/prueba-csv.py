#!/usr/bin/env python

#Importar datos de la base de datos a un archivo csv.

import csv

ifile  = open('ESCBASGENARINADUGARTEC.csv', "rb")
reader = csv.reader(ifile)
ofile  = open('ttest.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

for row in reader:
  writer.writerow(row)

ifile.close()
ofile.close()