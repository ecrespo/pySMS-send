#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Programa que captura los numeros de telefonos de un archivo, los nombres y
# el grupo de un archivo  csv y los guarda en una base de datos
#sqlite3.
"""
Autor: Ernesto Crespo
email: ecrespo@gmail.com
version: 0.1

"""

import re
def ValidarNumero(numero):
    #Valida si los numeros tienen 11 digitos y que sean de los proveedores movilnet, digitel y movistar
    if len(numero) == 11 and ((re.search("041[2|4|6]\d\d\d\d\d\d\d",numero)) or (re.search("042[4|6]\d\d\d\d\d\d\d",numero))) :
        return 1
    else:
        return 0
    
from sqlalchemy import *



def run(stmt):
    rs = stmt.execute()
    for row in rs:
        print row
        

#u = contactos.insert()

#u.execute(nombre='Luis Grisolia',telefono='04125673029',grupo_id=2)
#u.execute(nombre='Elizabeth Farrera',telefono='04148383838',grupo_id=2)

def Insertar(archivocsv):
    lineas = open(archivocsv,"r").readlines()
    lista = []
    for i in range(len(lineas)): 
        (grupo,cedula,nombre,telefono,direccion,psuv) = lineas[i][:-1].split(':')
        if len(telefono) < 10 or len(telefono) > 11:
            telefono = 'numero no valido'
        elif len(telefono) == 11 and ValidarNumero(telefono) == 0:
            telefono ='numero no valido'
        elif len(telefono) == 10 and ValidarNumero('0'+telefono) == 1:
            telefono = '0' + telefono
        if psuv.lower() == 'si':
            psuv = psuv.lower()
        elif psuv.lower() == 'no':
            psuv = psuv.lower()
        if psuv == "no":
            psuvb = False
        else:
            psuvb = True
        lista.append((grupo,cedula,nombre,telefono,direccion,psuvb))
        
    
    # Let's re-use the same database as before
    #db = create_engine('sqlite:///db5.db')
    db = create_engine('sqlite:///db5.db',convert_unicode=True, echo=False)
    #db.echo = False  
    # We want to see the SQL we're creating
    metadata = MetaData(db)
    # The users table already exists, so no need to redefine it. Just
    # load it from the database using the "autoload" feature.
    #$users = Table('users', metadata, autoload=True)
    contactos = Table('Contactos',metadata,autoload=True)
    grupos = Table('grupos',metadata,autoload=True)
    g = grupos.insert()
    
    
    g.execute(grupo=lista[1][0],descripcion=lista[1][0])
    
    
    
    
    
    c = contactos.insert()
    for i in range(1,len(lista)):
        print "Proceso : %s" %i
        r = grupos.select()
        rs = r.execute()
        for row in rs:
            if row[1] == lista[1][0]:
                identificador = row[0]
                break
                c.execute(nombre=lista[i][2].decode('utf-8'),cedula=lista[i][1],telefono=lista[i][3],direccion=lista[i][4],psuv=lista[i][5],grupo_id=row[0])
            else:
                continue
        c.execute(nombre=lista[i][2].decode('utf-8'),cedula=lista[i][1],telefono=lista[i][3],direccion=lista[i][4],psuv=lista[i][5],grupo_id=identificador)
        
            
    
        
        
    
    
    

if __name__ == "__main__":
    Insertar("ESCBASGENARINADUGARTEC.csv")