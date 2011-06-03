#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa grafico que permite enviar un mensaje de texto o multiples mensajes a celulares
License: GPLv3
Copyright: Copyright (C) 2011  Ernesto Nadir Crespo Avila
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@gmail.com
Version: 0.3
"""
#from future import *
from pyMensajeSend import Sms
from validadorCelNum import Validar
from deviceCell import Cell
from time import sleep
import centrosvotacion
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, inspect, sys
import string
import config
import commands

from commands import getstatusoutput

import threading
import thread
import gobject
#Iniciando el hilo sin usarlo
gtk.gdk.threads_init()


municipios ={ "Guaraque":{"Guaraque":[],"Mesa De Quintero":[],"Rio Negro":[]},
    "Sucre":{"Lagunillas":[],"Chiguara":[],"Estanques":[],"La Trampa":[],"Pueblo Nuevo del Sur":[],"San Juan":[]},
    "Aricagua":{"Aricagua":[],"San Antonio":[]},
    "Arzobispo Chacon":{"Canagua":[],"Capuri":[],"Chacanta":[],"El Molino":[],"Guaimaral":[],"Mucuchachi":[],"Mucutuy":[]},
    "Campo Elias":{"La Mesa":[],"Montalban":[],"San Jose":[],"Acequias":[],"Fernandez Pena":[],"Jaji":[],"Matriz":[]},
    "Padre Noguera": {"Santa Maria de Caparo":[]},
    "Rivas Davila":{"Bailadores":[],"Geronimo Maldonado":[]}}


class App(threading.Thread):
    def __init__(self):
        #Asignando a una variable el nombre del archivo glade
        self.__glade_file = "./sendSMS.glade"
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
	
	#Asignacion de combobox
	self.__ccentros = self.__w_tree.get_widget("ccentros")
	self.__cparroquias = self.__w_tree.get_widget("cparroquias")
	self.__cmunicipios = self.__w_tree.get_widget("cmunicipios")
	self.__cestructura = self.__w_tree.get_widget("cestructura")
	self.__cenviar = self.__w_tree.get_widget("cenviar")
	#Etiquetas
	self.__lcentro = self.__w_tree.get_widget("lcentro")
	self.__lparroquia = self.__w_tree.get_widget("lparroquia")
	self.__lmunicipio = self.__w_tree.get_widget("lmunicipio")
	self.__lestructura = self.__w_tree.get_widget("lestructura")
	self.__lenviar = self.__w_tree.get_widget("lenviar")
	
	
        
        self.__imagemenuitem5 = self.__w_tree.get_widget("imagemenuitem5")
        self.__imagemenuitem10 = self.__w_tree.get_widget("imagemenuitem10")
        #Asociacion de widgets con metodos.
        threading.Thread.__init__(self)
        self.__w_tree.signal_autoconnect(dict(inspect.getmembers(self)))
        #self.__lista_numeros = open("./numeros.txt","r").readlines()
        #self.__numeros = []
        #for i in range(len(self.__lista_numeros)):
        #    self.__numeros.append(self.__lista_numeros[i][:-1])
        #self.__cantidad_cel = len(self.__numeros)
        self.__cell = Cell("./config-sms.conf")
	self.__configuracion = config.config("./config-sms.conf")
	self.__responsable_nombre  = self.__configuracion.ShowValueItem("responsable","nombre")
	self.__responsable_celular = self.__configuracion.ShowValueItem("responsable","numero")
        self.__dispositivo,self.__baudios = self.__cell.InformacionDispositivo()
        self.__num_cel.show()
        self.__label2.show()
        self.__bandera_mensaje = 1
	#Bandera es 1.
	self.__num_cel.show()
	self.__mensaje.show()
	self.__label2.show()
	self.__lenviar.hide()
	self.__cenviar.hide()
	self.__lestructura.hide()
	self.__cestructura.hide()
	self.__lmunicipio.hide()
	self.__cmunicipios.hide()
	self.__lparroquia.hide()
	self.__cparroquias.hide()
	self.__lcentro.hide()
	self.__ccentros.hide()
	self.__municipio = ""
	self.__parroquia = ""
	self.__centro = ""
	self.__municipios_old = []
	self.__parroquias_old = []
	self.__centros_old = []
	
        self.__sms = Sms(self.__dispositivo,self.__baudios)
        
        self.__ventana1.show()
	self.__parroquias_old = []
	self.__centros_old = []

    
    def __agregar_numeros(self,archivo,flag):
	self.__lista_numeros = open(archivo,"r").readlines()
	if flag == 0:
	    self.__numeros = []
        for i in range(len(self.__lista_numeros)):
            self.__numeros.append(self.__lista_numeros[i][:-1])
    
    def on_cenviar_changed(self,*args):
	accion = self.__cenviar.get_active_text()
	self.__bandera_mensaje == 0
	if accion == "Estructura":
	    self.__lestructura.show()
	    self.__cestructura.show()
	    self.__lmunicipio.hide()
	    self.__cmunicipios.hide()
	    self.__lparroquia.hide()
	    self.__cparroquias.hide()
	    self.__ccentros.hide()
	    self.__lcentro.hide()
	elif accion == "Dependencias":
	    self.__lestructura.hide()
	    self.__cestructura.hide()
	    self.__lmunicipio.show()
	    self.__cmunicipios.show()
	    self.__lparroquia.hide()
	    self.__cparroquias.hide()
	    self.__lcentro.hide()
	    self.__ccentros.hide()
    
    def on_cestructura_changed(self,*args):
	self.__bandera_mensaje = 0
	accion = self.__cestructura.get_active_text()
	if accion == "Todos":
	    self.__agregar_numeros("jefepatrullas.txt",0)
	    self.__agregar_numeros("uubb200.txt",1)
	    self.__cantidad_cel = len(self.__numeros)
	elif accion == "Jefe de Patrullas":
	    self.__agregar_numeros("jefepatrullas.txt",0)
	    self.__cantidad_cel = len(self.__numeros)
	elif accion == "UUBB200":
	    self.__agregar_numeros("uubb200.txt",0)
	    self.__cantidad_cel = len(self.__numeros)

    
    def on_cmunicipios_changed(self,*args):
	self.__municipio = self.__cmunicipios.get_active_text()
	if self.__municipio <> "Todos":
	    self.__lparroquia.show()
	    self.__cparroquias.show()
	    self.__lcentro.hide()
	    self.__ccentros.hide()
	    self.__parroquias = municipios[self.__municipio].keys()
	    if self.__cparroquias.get_active() == -1 :
		for parroquia in self.__parroquias:
		    self.__cparroquias.append_text(parroquia)
		self.__parroquias_old = self.__parroquias
	    else:
		for i in range(1,len(self.__parroquias_old)+1): self.__cparroquias.remove_text(1)
		self.__parroquias_old = self.__parroquias
		for parroquia in self.__parroquias:
		    self.__cparroquias.append_text(parroquia)
	else:
	    #getstatusoutput("rm numeros1.txt")
	    self.__lparroquia.hide()
	    self.__cparroquias.hide()
	    self.__lcentro.hide()
	    self.__ccentros.hide()
	    self.__todos("./centros/*.txt")
	    self.__agregar_numeros("numeros1.txt",0)
    
    def __todos(self,patron):
	resultado = getstatusoutput("for i in $(ls %s);do cat $i >> numeros1.txt; done" %patron)
	if resultado[0] == 0:
	    print "Todo bien"
	else:
	    print "Un error"
	    
	
    
    def on_cparroquias_changed(self,*args):
	self.__parroquia = self.__cparroquias.get_active_text()
	listado = centrosvotacion.ListarCentro("centrosvotacion.csv")
	if self.__parroquia <> "Todos":
	    self.__lcentro.show()
	    self.__ccentros.show()
	    if self.__ccentros.get_active() == -1:
		for lista in listado:
		    if string.find(lista[0],self.__municipio.lower()) <> -1:
			if string.find(lista[1],self.__parroquia.lower()) <> -1:
			    self.__ccentros.append_text(lista[2])
			    self.__centros_old.append(lista[2])
	    else:
		for i in range(1,len(self.__centros_old)+1): self.__ccentros.remove_text(1)
		for lista in listado:
		    if string.find(lista[0],self.__municipio.lower()) <> -1:
			if string.find(lista[1],self.__parroquia.lower()) <> -1:
			    self.__ccentros.append_text(lista[2])
			    self.__centros_old.append(lista[2])
	else:
	    #getstatusoutput("rm numeros1.txt")
	    self.__lcentro.hide()
	    self.__ccentros.hide()
	    self.__todos("./centros/%s.*.*.txt" %(self.__municipio.lower()))
	    self.__agregar_numeros("numeros1.txt",0)
    
    def on_ccentros_changed(self,*args):
	self.__centro = self.__ccentros.get_active_text()
	if self.__centro <> "Todos":
	    centros= self.__centro.split(" ")
	    centro = ""
	    for i in range(len(centros)):
		if self.__centro[i] <> "":
		    centro = centro + centros[i]
	    self.__centro = centro.lower().split(" ")[0]
	    if string.find(self.__municipio," ") <> -1:
		municipios = self.__municipio.split(" ")
		municipio = ""
		for i in range(len(municipios)):
		    if municipios[i] <> "":
			municipio = municipio + municipios[i]
		self.__municipio = municipio
		
	    if string.find(self.__parroquia," ") <> -1:
		parroquias = self.__parroquia.split(" ")
		parroquia = ""
		for i in range(len(parroquias)):
		    if parroquias[i] <> "":
			parroquia = parroquia + parroquias[i]
		self.__parroquia = parroquia
	    resultado = commands.getstatusoutput("ls ./centros/%s.%s.*" %(self.__municipio.lower(),self.__parroquia.lower()))
	    archivos = resultado[1].split("\n")
	    Municipios = []
	    Parroquias =  []
	    Centros =  []
	    for i in range(len(archivos)):
		Municipios.append(archivos[i].split("/")[2].split(".")[0])
		Parroquias.append(archivos[i].split("/")[2].split(".")[1])
		Centros.append(archivos[i].split("/")[2].split(".")[2])
	    for i in range(len(archivos)):
		if Municipios[i] == self.__municipio.lower():
		    if Parroquias[i] == self.__parroquia.lower():
			if string.find(self.__centro.lower(),Centros[i]) <> -1:
			    result = i
			    break
			else:
			    result = -1
	    if result <> -1:
		self.__agregar_numeros(archivos[result],0) 
	else:
	    getstatusoutput("rm numeros1.txt")
	    self.__todos("./centros/%s.%s.*.txt" %(self.__municipio.lower(),self.__parroquia.lower()))
	    self.__agregar_numeros("numeros1.txt",0)
	

    
    
    def on_salir_clicked(self,*args):
        gtk.main_quit()
        sys.exit(1)
    
    def on_imagemenuitem5_activate(self,*args):
        gtk.main_quit()
        sys.exit(1)
    
    def on_imagemenuitem10_activate(self,*args):
        result = self.__acercade.run()
        if result: self.__acercade.hide()

            
    def on_ejecutar_clicked(self, *args):
        lock =  thread.allocate_lock()
        lock.acquire()
        thread.start_new_thread( self.__ejecucion, ())
        lock.release()
        #self.__ejecucion()
                
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
		sleep(3.5)
		self.__sms.SendMensaje(self.__responsable_celular,"%s, se ha enviado el mensaje a %s" %(self.__responsable_nombre,self.__celular))
        else:
           
            #Multiples mensajes
	    self.__cantidad_cel = len(self.__numeros)
            for i in range(len(self.__numeros)):
                if Validar(self.__numeros[i]) == 0:
                    self.__resultado.set_text("Mensaje %s/%s - %s no es un numero valido" %(i+1,self.__cantidad_cel,self.__numeros[i]))
                else:
                    self.__sms.SendMensaje(self.__numeros[i],self.__texto)
                    sleep(3.5)
                    self.__resultado.set_text("Mensaje %s/%s - Mensaje enviado al %s" %(i+1,self.__cantidad_cel,self.__numeros[i]))
	    sleep(3.5)
	    self.__sms.SendMensaje(self.__responsable_celular,"%s, se ha enviado los %s" %(self.__responsable_nombre,self.__cantidad_cel))
        self.__resultado.set_text("Fin de envio de mensajes")        
        
    def on_ventana1_destroy(self,*args):
        gtk.main_quit()
        sys.exit(1)

        

        
    def on_multiple_toggled(self,*args):
        self.__num_cel.hide()
        self.__label2.hide()
	self.__cenviar.show()
	self.__lenviar.show()
	self.__cestructura.hide()
	self.__lestructura.hide()
	self.__lmunicipio.hide()
	self.__cmunicipios.hide()
	self.__lparroquia.hide()
	self.__cparroquias.hide()
	self.__ccentros.hide()
	self.__lcentro.hide()
        self.__bandera_mensaje = 0
        
    def on_sencillo_toggled(self,*args):
        self.__num_cel.show()
        self.__label2.show()
	self.__cenviar.hide()
	self.__lenviar.hide()
	self.__cestructura.hide()
	self.__lestructura.hide()
	self.__lmunicipio.hide()
	self.__cmunicipios.hide()
	self.__lparroquia.hide()
	self.__cparroquias.hide()
	self.__ccentros.hide()
	self.__lcentro.hide()
        self.__bandera_mensaje = 1
            
        
    def main(self):
	gtk.main()
            

if __name__ == "__main__":
    app = App()
    app.main()
    
