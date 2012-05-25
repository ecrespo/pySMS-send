#!/usr/bin/env python

#Importar datos de la base de datos a un archivo csv.

import csv
from sqlalchemy import *



    

def run(stmt):
    rs = stmt.execute()
    for row in rs:
        print row
        

def Exportar(archivocsv,bdatos):
    ofile = open(archivocsv, "wb")
    db = create_engine('sqlite:///%s' %bdatos,convert_unicode=True, echo=False)
    metadata = MetaData(db)
    contactos = Table('Contactos',metadata,autoload=True)
    grupos = Table('grupos',metadata,autoload=True)
    
    s = select([contactos.c.nombre,contactos.c.cedula,contactos.c.telefono,contactos.c.direccion, grupos.c.grupo, contactos.c.psuv], grupos.c.id == contactos.c.grupo_id )
    rs = s.execute()
    ofile  = open(archivocsv, "wb")
    writer = csv.writer(ofile, delimiter='\t', quotechar=':', quoting=csv.QUOTE_ALL)
    lista = []
    i = 1
    for row in rs:
        print i
        writer.writerow([row[0].encode('utf-8'),row[1],row[2],row[3],row[4],row[5]])
        #writer.writerow(row)
        i = i +1
    ofile.close()

    
if __name__ == '__main__':
    Exportar("prueba.csv","db5.db")
    