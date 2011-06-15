#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa que permite validar numeros de telefono celular para las companias movistar, digitel y movilnet.
License: GPLv3
Copyright: Copyright (C) 2011 Ernesto Nadir Crespo Avila
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
Version: 0.2
"""

import re
def Validar(numero):
    """
    Devuelve 1 si el numero es valido,
    devuelve 0 si el numero no es valido.
    """
    #Valida si los numeros tienen 11 digitos y que sean de los proveedores movilnet, digitel y movistar
    if len(numero) == 11 and ((re.search("041[2|4|6]\d\d\d\d\d\d\d",numero)) or (re.search("042[4|6]\d\d\d\d\d\d\d",numero))) :
        return 1
    else:
        return 0


