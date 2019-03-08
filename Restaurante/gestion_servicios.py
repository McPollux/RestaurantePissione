#from Restaurante.declaraciones import piss import --- Redundante ya que ya es importando en Restaurante.cargas
from Restaurante.cargas import *


def altaServicio(widget):
    """
     Evento que se lanza al darle al boton correspondiente en la interfaz, realiza el alta y limpia los campos.
    """
    if piss.etNomServ.get_text() != "":
        if piss.etPrecioUniServ.get_text().replace('.', '', 1).isdigit():
            lista = (piss.etNomServ.get_text(), piss.etPrecioUniServ.get_text())

            piss.curRestaurante.execute("insert into servicios (nombre, precio) values (?, ?)", lista)
            piss.conexPissione.commit()

            piss.etNomServ.set_text("")
            piss.etPrecioUniServ.set_text("")
            piss.lblErrorServ.set_text("")
            cargarServicios()
        else:
            piss.lblErrorServ.set_text("El precio debe ser un número")
    else:
        piss.lblErrorServ.set_text("El nombre no puede estar vacio")


def bajaServicio(widget):
    """
     Evento que borra un servicio al darle al boton correspondiente en la interfaz, solo realizará esta tarea en caso
     de que dicho servicio no esté ya asociado a alguna factura.
    """
    a = piss.treeServicios.get_selection()
    (tm, ti) = a.get_selected()

    piss.curRestaurante.execute("select idComanda from lineasfactura where idServicio = \'" + str(tm.get_value(ti, 0)) + "\'")
    lista = piss.curRestaurante.fetchall()

    if len(lista) > 0:
        piss.lblErrorServ.set_text("Este servicio ya está asociado a una comanda, no puede ser eliminado.")
    else:
        piss.curRestaurante.execute("delete from servicios where idServicio = \'" + str(tm.get_value(ti, 0)) + "\'")
        piss.conexPissione.commit()

        cargarServicios()
        piss.lblErrorServ.set_text("")

#EOF