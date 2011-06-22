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
    def __init__(self,celular,configuracion,conexion):
        """
        Se capturan los valores del archivo de configuracion y se asigna los valores a
        los datos del objeto Cell
        """
        self.__celular = celular
        self.__configparser = config.config(configuracion)
        self.__conexionAndroid = conexion
        if self.__celular == "android":
            self.__adb = self.__configparser.ShowValueItem("android","ruta_adb")
        elif celular == "v9":
            self.__dispositivo = self.__configparser.ShowValueItem("dispositivo","dispositivo")
            self.__baudios = self.__configparser.ShowValueItem("dispositivo","baudios")
        
        
    def DispositivoNoExiste(self):
        """Si el dispositivo no existe devuelve 1
        si existe devuelve 0
        """
        if self.__celular == "v9":
            if not (path.isfile(self.__dispositivo)):
                return 1
            else:
                return 0
        elif self.__celular == "android" and self.__conexionAndroid == "usb":
            from commands import getstatusoutput
            r = getstatusoutput("%s devices" %self.__adb)
            if r[0] == 0:
                #Se inicio el dispositivo sin problemas
                l = r[1].split("\n")
                if l[1] <> '':
                    return 0
                else:
                    return 1
            else:
                return 1
        elif self.__celular == "android" and self.__conexionAndroid == "wifi":
            return 1
        
    
            
    def LevantarDispositivo(self):
        """
        Se configura el dispositivo asi sea android o el motorola V9
        Devuelve 1 si todo se configuro correctamente.
        Devuelve 0 si no se logro configurar correctamente el dispositivo
        """
        if self.__celular == "v9":
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
        elif self.__celular == "android" and self.__conexionAndroid == "usb":
            #Se ejecuta adb devices
            r = getstatusoutput("%s devices" %self.__adb)
            if r[0] == 0:
                l = r[1].split("\n")
                if l[1] <> '':
                    return 1
                else:
                    return 0
            else:
                return 0
        elif self.__celular == "android" and self.__conexionAndroid == "wifi":
            return 0
        
        
    
    def InformacionDispositivo(self):
        if self.__celular == "v9":
            info_dispositivo = (self.__dispositivo,self.__baudios)
        elif self.__celular == "android" and self.__conexionAndroid == "usb":
            r = getstatusoutput("%s devices" %self.__adb)
            if r[0] == 0:
                info_dispositivo = ("android","usb",self.__adb,r[1].split("\n")[1].split("\tdevice")[0])
        elif self.__celular == "android" and self.__conexionAndroid == "wifi":
            info_dispositivo = ("android","wifi",self.__adb)
        return info_dispositivo 
            

if __name__ == "__main__":
    cel = Cell("android","./config-sms.conf","usb")
    print "iniciando la deteccion"
    if cel.DispositivoNoExiste() == 0 :
        print "El dispositivo existe:",cel.InformacionDispositivo()
    else:
        print "levantando el dispositivo"
        resultado = cel.LevantarDispositivo()
        if resultado == 0:
            print "no se pudo detectar el dispositivo android"
        else:
            print "El dispositivo existe:",cel.InformacionDispositivo()
    
