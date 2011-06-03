#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Modulo que permite enviar mensajes de texto desde consola
License: GPLv3
Copyright: Copyright (C) 2011 Ernesto Nadir Crespo Avila
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
version: 0.2
"""
import serial
#Se define la clase SMS
class Sms:
    def __init__(self,dispositivo,baudios):
        #Se define el modo del celular
        self.__modo = "AT+MODE=2\r\n"
        #Se define el envio de mensajes en ascii
        self.__te = "AT+CSCS=ASCII\r\n"
        #Asignacion de valores del puerto serial
        self.__dispositivo_serial = dispositivo
        self.__baudios = baudios
        #Se asocia la instancia del puerto serial con sus parametros
        self.__serial = serial.Serial(self.__dispositivo_serial,self.__baudios,timeout=0.7)
        #Se abre el puerto,se escribe el modo y el formato ascii para los mensajes
        self.__serial.open()
        self.__serial.write(self.__modo)
        self.__serial.write(self.__te)
        
    
    def SendMensaje(self,numero,mensaje):
        #Se envie el comando at para definir el numero de celular a enviar el mensaje
        self.__msg1  = "AT+CMGS=\"%s\"\r" %numero
        self.__msg2 = mensaje
        #Se le agrega al mensaje el caracter 26 control z.
        self.__msg2 = self.__msg2 + chr(26)
        #Se envie el mensaje
        self.__serial.write(self.__msg1)
        self.__serial.write(self.__msg2)
        

if __name__ == "__main__":
    sms = Sms("/dev/ttyUSB0",19200)
    sms.SendMensaje("numero","esta es una prueba")
    pass

