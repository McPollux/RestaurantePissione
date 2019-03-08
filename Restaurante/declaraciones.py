import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from Restaurante.Mesas import Mesas

import datetime
import sqlite3

class piss:
    b = Gtk.Builder()
    b.add_from_file('Restaurante.glade')
    try:
        bbdd = 'pissione.sqlite'  # variable almacena base de datos
        conexPissione = sqlite3.connect(bbdd)
        curRestaurante = conexPissione.cursor()
        curRestaurante.execute("PRAGMA foreign_keys = ON")
        conexPissione.commit()
        # le conectamos el cursor
    except sqlite3.OperationalError as e:
        print(e)

    try:
        reverb = 'act17.sqlite'  # variable almacena base de datos
        conexReverb = sqlite3.connect(reverb)
        curReverb = conexReverb.cursor()
        # le conectamos el cursor
    except sqlite3.OperationalError as e:
        print(e)

    notebook = b.get_object("notebook")
    priWin = b.get_object("PriWin")

    # Login
    gbLogin = b.get_object("gbLogin")
    etUsuario = b.get_object("etUsuario")
    etContrasenha = b.get_object("etContrasenha")
    lblErrorLogin = b.get_object("lblErrorLogin")
    btnEntrar = b.get_object("btnEntrar")
    camarero = "Jordi Auxiliar"

    # Mesas
    venprincipal = b.get_object("PriWin")
    btnMesa1 = b.get_object("btnMesa1")
    btnMesa2 = b.get_object("btnMesa2")
    btnMesa3 = b.get_object("btnMesa3")
    btnMesa4 = b.get_object("btnMesa4")
    btnMesa5 = b.get_object("btnMesa5")
    btnMesa6 = b.get_object("btnMesa6")
    btnMesa7 = b.get_object("btnMesa7")
    btnMesa8 = b.get_object("btnMesa8")
    mesaAzul = -1

    verdeMesa1 = b.get_object("verdeMesa1")
    azulMesa1 = b.get_object("azulMesa1")
    rojoMesa1 = b.get_object("rojoMesa1")
    verdeMesa2 = b.get_object("verdeMesa2")
    azulMesa2 = b.get_object("azulMesa2")
    rojoMesa2 = b.get_object("rojoMesa2")
    verdeMesa3 = b.get_object("verdeMesa3")
    azulMesa3 = b.get_object("azulMesa3")
    rojoMesa3 = b.get_object("rojoMesa3")
    verdeMesa4 = b.get_object("verdeMesa4")
    azulMesa4 = b.get_object("azulMesa4")
    rojoMesa4 = b.get_object("rojoMesa4")
    verdeMesa5 = b.get_object("verdeMesa5")
    azulMesa5 = b.get_object("azulMesa5")
    rojoMesa5 = b.get_object("rojoMesa5")
    verdeMesa6 = b.get_object("verdeMesa6")
    azulMesa6 = b.get_object("azulMesa6")
    rojoMesa6 = b.get_object("rojoMesa6")
    verdeMesa7 = b.get_object("verdeMesa7")
    azulMesa7 = b.get_object("azulMesa7")
    rojoMesa7 = b.get_object("rojoMesa7")
    verdeMesa8 = b.get_object("verdeMesa8")
    azulMesa8 = b.get_object("azulMesa8")
    rojoMesa8 = b.get_object("rojoMesa8")

    listComandas1 = b.get_object("listComandas1")
    listComandas2 = b.get_object("listComandas2")
    listComandas3 = b.get_object("listComandas3")
    listComandas4 = b.get_object("listComandas4")
    listComandas5 = b.get_object("listComandas5")
    listComandas6 = b.get_object("listComandas6")
    listComandas7 = b.get_object("listComandas7")
    listComandas8 = b.get_object("listComandas8")

    listas = (
        listComandas1, listComandas2, listComandas3, listComandas4, listComandas5,
        listComandas6, listComandas7, listComandas8)

    mesas = (
        Mesas(), Mesas(), Mesas(), Mesas(),
        Mesas(), Mesas(), Mesas(), Mesas())

    # Facturas
    listProvincias = b.get_object("listProvincias")
    listMunicipios = b.get_object("listMunicipios")
    listSelServicios = b.get_object("listSelServicios")
    gbFactura = b.get_object("gbFactura")
    lblMesa = b.get_object("lblMesa")
    lblCamarero = b.get_object("lblCamarero")
    lblFecha = b.get_object("lblFecha")
    etDni = b.get_object("etDni")
    etNombre = b.get_object("etNombre")
    etApellidos = b.get_object("etApellidos")
    etDireccion = b.get_object("etDireccion")
    cmbProvincia = b.get_object("cmbProvincia")
    cmbCiudad = b.get_object("cmbCiudad")
    treeComandas = b.get_object("treeComandas")
    treeSelServicios = b.get_object("treeSelServicios")
    lblTotal = b.get_object("lblTotal")
    lblError = b.get_object("lblError")
    booleanCliente = False

    # Administracion
    nbAdministracion = b.get_object("nbAdministracion")

    treeFacturas = b.get_object("treeFacturas")
    treeNoFuncional = b.get_object("treeNoFuncional")
    treeLineasFactura = b.get_object("treeLineasFactura")
    listLineasFactura = b.get_object("listLineasFactura")

    listFacturas = b.get_object("listFacturas")
    listClientes = b.get_object("listClientes")
    listCamareros = b.get_object("listCamareros")
    listMesas = b.get_object("listMesas")

    treeClientes = b.get_object("treeClientes")
    etDniAdm = b.get_object("etDniAdm")

    etNombreAdm = b.get_object("etNombreAdm")
    etApellidosAdm = b.get_object("etApellidosAdm")
    etDireccionAdm = b.get_object("etDireccionAdm")
    cmbProvinciaAdm = b.get_object("cmbProvinciaAdm")
    cmbCiudadAdm = b.get_object("cmbCiudadAdm")
    listProvincias2 = b.get_object("listProvincias2")
    listMunicipios2 = b.get_object("listMunicipios2")
    lblErrorClientes = b.get_object("lblErrorClientes")

    etIdFactura = b.get_object("etIdFactura")
    etDni2 = b.get_object("etDni2")
    etFecha = b.get_object("etFecha")

    treeServicios = b.get_object("treeServicios")
    treeSelServicio = b.get_object("treeSelServicio")
    etNomServ = b.get_object("etNomServ")
    etPrecioUniServ = b.get_object("etPrecioUniServ")
    lblErrorServ = b.get_object("lblErrorServ")

#EOF
