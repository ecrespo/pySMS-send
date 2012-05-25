#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Se importa sqlalchemy
from sqlalchemy import *

#Se crea la instancia del motor de la base de datos y se asocia con un
#archivo
db = create_engine('sqlite:///db5.db', convert_unicode=True, echo=True)
#se coloca la base de datos en modo no mostrar resultados 
#de las instrucciones en pantalla.
db.echo = False

#Se asocia el archivo de la base de datos a la instancia de metadatos.
metadata = MetaData(db)

contactos = Table(
    'contactos',metadata,
    Column('id',Integer,primary_key=True),
    Column('nombre', Unicode(100)),
    Column('cedula', Integer),
    Column('telefono',String(11)),
    Column('direccion',Unicode(200)),
    Column('psuv',Boolean),
    Column('grupo_id', ForeignKey('grupos.id'))
    )

#Se crea la tabla de grupos tal cual el mismo ejemplo de 
#sqlite


grupos = Table(
    'grupos',metadata,
    Column('id',Integer,primary_key=True),
    Column('grupo',Unicode(300)),
    Column('descripcion',Unicode(500))
)




#Se crea todas las tablas.
metadata.create_all()

