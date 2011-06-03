#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa que permite enviar mensajes de texto via consola

License: GPLv3
Copyright: Copyright (C) 2011 Ernesto Nadir Crespo Avila
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
version: 0.2

"""

from pyMensajeSend import Sms
from validadorCelNum import Validar
from deviceCell import Cell
from time import sleep

class Mensaje:
    def __init__(self):
        self.__celular = Cell("./config-sms.conf")

        self.__dispositivo,self.__baudios = self.__celular.InformacionDispositivo()
        self.__mensaje = ""
        self.__numeros = []
        if self.__celular.DispositivoNoExiste() <> 0:
            print "Desconecte y conecte el celular"
            self.__celular.LevantarDispositivo()
        self.__sms = Sms(self.__dispositivo,self.__baudios)
           
    def Enviar(self,mensaje,numero):
        if Validar(numero) == 0:
            print "Agregue un numero de telefono valido"
        self.__sms.SendMensaje(numero,mensaje)
    
    def EnviarMultiples(self,mensaje,numeros):
        self.__lista_numeros =open(numeros,'r').readlines()
        for i in range(len(self.__lista_numeros)):
            if Validar(self.__lista_numeros[i][:-1]) == 0:
                print "Verifique el numero de telefono:%s" %self.__lista_numeros[i][:-1]
                continue
            self.__numeros.append(self.__lista_numeros[i][:-1])
        
        for num_cel in self.__numeros:
            self.__sms.SendMensaje(num_cel,mensaje)
            sleep(4)
            print "Enviado mensaje al numero %s" %num_cel
    
if __name__ == "__main__":
    mensaje = Mensaje()
    #mensaje.Enviar("pong","numero")
    #mensaje.EnviarMultiples("Segunda prueba a las 10:25am","./numeros.txt")
    #mensaje.EnviarMultiples("Saludos camaradas, mensaje enviado desde Linux","./numeros.txt")
    #Importar m?dulo argparse para capturar los argumentos del comando    
    import argparse
    acciones = ["configurar","enviarMensaje","enviarMultiMensajes"]
    #Creaci?n del parse 
    parser = argparse.ArgumentParser(prog='sms-send',description="Programa que envia mensajes de texto desde Linux por el Celular")
    parser.add_argument('-a','--accion',type=str,choices=acciones,default=acciones,help='Acciones de sms-send')
    
    
