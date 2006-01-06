#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa que permite validar numeros de telefono celular para las compa?ias movistar, digitel y movilnet.
License: GPLv3
Copyright: Copyright (C) 2009  Distrito Socialista Tecnologico AIT PDVSA M?rida
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
Version: 0.1
"""

import re
def Validar(numero):
    if len(numero) == 11 and ((re.search("041[2|4|6]\d\d\d\d\d\d\d",numero)) or (re.search("042[4|6]\d\d\d\d\d\d\d",numero))) :
        return 1
    else:
        return 0


