#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Programa que permite enviar mensajes de texto via consola

License: GPLv3
Copyright: Copyright (C) 2009  Distrito Socialista Tecnologico AIT PDVSA M?rida
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com

"""
import serial

class Sms:
    def __init__(self,dispositivo,baudios):
        
        self.__modo = "AT+MODE=2\r\n"
        self.__te = "AT+CSCS=ASCII\r\n"
        self.__dispositivo_serial = dispositivo
        self.__baudios = baudios
        self.__serial = serial.Serial(self.__dispositivo_serial,self.__baudios,timeout=0.7)
        self.__serial.open()
        self.__serial.write(self.__modo)
        self.__serial.write(self.__te)
        
    
    def SendMensaje(self,numero,mensaje):
        self.__msg1  = "AT+CMGS=\"%s\"\r" %numero
        self.__msg2 = mensaje
        self.__msg2 = self.__msg2 + chr(26)
        self.__serial.write(self.__msg1)
        self.__serial.write(self.__msg2)
        

if __name__ == "__main__":
    #sms = Sms("/dev/ttyUSB0",19200)
    #sms.SendMensaje("numero","esta es una prueba")
    pass

