#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Name: su
Description: Modulo que permite la ejecución de comandos como root
Version:0.1
License: GPLv3
Copyright: Copyright (C) 2009 Proyecto Libre Accesibilidad - Distrito Socialista Tecnologico AIT PDVSA  <moderador@libreaccesibilidad.org>
Author: Ernesto Nadir Crespo Avila
Email: ernesto@libreaccesibilidad.org
"""


import pdb
import gksu2 as gksu
import gobject
import getpass
from commands import getstatusoutput


def ask_pass_func(context, prompt):
    try:
        r = getstatusoutput("mpg123 voces/11.mp3")
        return getpass.getpass("Escriba la clave de administrador (root): ")
    except KeyboardInterrupt:
        print
        err = gobject.GError("keyboard interrupt")
        err.code = gksu.ERROR_CANCELED
        err.domain = "libgksu"
        raise err

def ejecutar(comando):
    ctx = gksu.Context()
    ctx.set_command(comando)
    gksu.su_full(ctx, ask_pass=ask_pass_func)
    
def AgregarUsuarioSudo(usuario):
    ejecutar("echo \"%s ALL=(ALL) ALL\" >>  /etc/sudoers " %usuario)
    

    
    
if __name__ == "__main__":
    ejecutar("ls -la /root")
    ejecutar("cd /root ; pwd")
