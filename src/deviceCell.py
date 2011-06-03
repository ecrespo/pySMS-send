#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: privilegios
Description: Modulo que permite detectar que el dispositivo este conectado y si no se reconfigura, adicionalmente pasa la informacion
del dispositivo.

Version:0.2
License: GPLv3
Copyright: Copyright (C) Ernesto Nadir Crespo Avila
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
"""
import config
from os import path
from privilegios import ejecutar, AgregarUsuarioSudo
from commands import getstatusoutput

class Cell:
    def __init__(self,configuracion):
        self.__configparser = config.config(configuracion)
        self.__dispositivo = self.__configparser.ShowValueItem("dispositivo","dispositivo")
        self.__baudios = self.__configparser.ShowValueItem("dispositivo","baudios")
        
        
    def DispositivoNoExiste(self):
        if not (path.isfile(self.__dispositivo)):
            return 0
        else:
            return 1
            
    def LevantarDispositivo(self):
        ejecutar("modprobe usbserial vendor=0x22b8 product=0x2b24")
        resultado = getstatusoutput("ls /dev/ttyUSB*")
        if resultado[0] <> 0:
            return 0
        dispositivo_nuevo = resultado[1].split("\n")[0]
        if self.__dispositivo <> dispositivo_nuevo:
            self.__configparser.change("dispositivo","dispositivo",dispositivo_nuevo)
            self.__dispositivo = dispositivo_nuevo
            self.__configparser.write()
        return 1
        
        
    
    def InformacionDispositivo(self):
        info_dispositivo = (self.__dispositivo,self.__baudios)
        return info_dispositivo 
            

if __name__ == "__main__":
    cel = Cell("./config-sms.conf")
    print cel.DispositivoNoExiste()
    cel.LevantarDispositivo()
    
