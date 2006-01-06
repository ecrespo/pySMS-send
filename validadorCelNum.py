#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa que permite validar numeros de telefono celular para las companias movistar, digitel y movilnet.
License: GPLv3
Copyright: Copyright (C) 2010  Distrito Socialista Tecnologico AIT PDVSA Merida
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
Version: 0.1
"""

import re
def Validar(numero):
    #Valida si los numeros tienen 11 digitos y que sean de los proveedores movilnet, digitel y movistar
    if len(numero) == 11 and ((re.search("041[2|4|6]\d\d\d\d\d\d\d",numero)) or (re.search("042[4|6]\d\d\d\d\d\d\d",numero))) :
        return 1
    else:
        return 0


