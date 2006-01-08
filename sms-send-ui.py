#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa grafico que permite enviar un mensaje de texto o multiples mensajes a celulares
License: GPLv3
Copyright: Copyright (C) 2010  Distrito Socialista Tecnologico AIT PDVSA Merida
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
Version: 0.1
"""

from pyMensajeSend import Sms
from validadorCelNum import Validar
from deviceCell import Cell
from time import sleep
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, inspect, sys

#
import threading
import thread
import gobject
#Iniciando el hilo sin usarlo
gtk.gdk.threads_init()

class App:
    def __init__(self):
        #Asignando a una variable el nombre del archivo glade
        self.__glade_file = "./sendSMS2.glade"
        self.__w_tree = gtk.glade.XML(self.__glade_file)
        # Asociando las ventanas
        self.__ventana1 = self.__w_tree.get_widget('ventana1')
        self.__acercade = self.__w_tree.get_widget("acercade")
        self.__aviso    = self.__w_tree.get_widget("aviso")
        
        self.__mensaje = self.__w_tree.get_widget("mensaje")
        self.__num_cel = self.__w_tree.get_widget("numcel")
        self.__cargarconfig = self.__w_tree.get_widget("cargarconfig")
        self.__sencillo = self.__w_tree.get_widget("sencillo")
        self.__multiple = self.__w_tree.get_widget("multiple")
        self.__ejecutar = self.__w_tree.get_widget("ejecutar")
        self.__salir = self.__w_tree.get_widget("salir")
        self.__label2 = self.__w_tree.get_widget("label2")
        self.__resultado = self.__w_tree.get_widget("resultado")
        
        self.__imagemenuitem5 = self.__w_tree.get_widget("imagemenuitem5")
        self.__imagemenuitem10 = self.__w_tree.get_widget("imagemenuitem10")
        #Asociacion de widgets con metodos.
        
        self.__w_tree.signal_autoconnect(dict(inspect.getmembers(self)))
        self.__lista_numeros = open("./numeros.txt","r").readlines()
        self.__numeros = []
        for i in range(len(self.__lista_numeros)):
            self.__numeros.append(self.__lista_numeros[i][:-1])
        self.__cantidad_cel = len(self.__numeros)
        self.__cell = Cell("./config-sms.conf")
        self.__dispositivo,self.__baudios = self.__cell.InformacionDispositivo()
        self.__num_cel.show()
        self.__label2.show()
        self.__bandera_mensaje = 1
        self.__sms = Sms(self.__dispositivo,self.__baudios)
        self.__ventana1.show()

            
    def on_salir_clicked(self,*args):
        gtk.main_quit()
        sys.exit(1)
    
    def on_imagemenuitem5_activate(self,*args):
        gtk.main_quit()
        sys.exit(1)
    
    def on_imagemenuitem10_activate(self,*args):
        result = self.__acercade.run()
        if result: self.__acercade.hide()

    
    def on_cargarconfig_clicked(self,*args):
        if self.__cell.DispositivoNoExiste() == 0:
            self.__aviso.set_title("Error")
            self.__aviso.set_markup("El modulo del celular no esta cargado, desconecte el celular, conectelo y vuelva a ejecutar la configuracion ")    
            result =self.__aviso.run()
            if result: self.__aviso.hide()
            if self.__cell.LevantarDispositivo() == 0:
                self.__aviso.set_title("Error")
                self.__aviso.set_markup("No se deteta el dispositivo")
                result =self.__aviso.run()
                if result: self.__aviso.hide()
            else:
                self.__aviso.set_title("Funciona")
                self.__aviso.set_markup("Se levanto la configuracion")
                result =self.__aviso.run()
                if result: self.__aviso.hide()
        else:
            self.__aviso.set_title("Funciona")
            self.__aviso.set_markup("Se levanto la configuracion")
            result =self.__aviso.run()
            if result: self.__aviso.hide()
                
            
    def on_ejecutar_clicked(self, *args):
        self.__ejecucion()
                
    def __ejecucion(self,*args):
        self.__resultado.set_text("")
        self.__texto = self.__mensaje.get_text()
        if self.__bandera_mensaje == 1:
            self.__celular = self.__num_cel.get_text()
            if Validar(self.__celular) == 0:
                self.__resultado.set_text("%s no es un numero valido" %self.__celular)
            else:
                self.__sms.SendMensaje(self.__celular,self.__texto)
                self.__resultado.set_text("Mensaje enviado al %s" %self.__celular)
        else:
            #Multiples mensajes
            for i in range(len(self.__numeros)):
                if Validar(self.__numeros[i]) == 0:
                    self.__resultado.set_text("Mensaje %s/%s - %s no es un numero valido" %(i+1,self.__cantidad_cel,self.__numeros[i]))
                else:
                    self.__sms.SendMensaje(self.__numeros[i],self.__texto)
                    sleep(3.5)
                    self.__resultado.set_text("Mensaje %s/%s - Mensaje enviado al %s" %(i+1,self.__cantidad_cel,self.__numeros[i]))
        self.__resultado.set_text("Fin de envio de mensajes")        
        
    def on_ventana1_destroy(self,*args):
        gtk.main_quit()
        sys.exit(1)

        

        
    def on_multiple_toggled(self,*args):
        self.__num_cel.hide()
        self.__label2.hide()
        self.__bandera_mensaje = 0
        
    def on_sencillo_toggled(self,*args):
        self.__num_cel.show()
        self.__label2.show()
        self.__bandera_mensaje = 1
            
        
    def main(self):
	gtk.main()
            

if __name__ == "__main__":
    app = App()
    app.main()
    