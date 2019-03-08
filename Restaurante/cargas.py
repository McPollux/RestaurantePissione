from Restaurante.declaraciones import piss
import sqlite3

def cargarServicios():
    """
    Al iniciarse el programa carga todos los servicios en la lista compartida por la aplicación.
    """
    piss.curRestaurante.execute("select * from Servicios")
    lista = piss.curRestaurante.fetchall()
    piss.listSelServicios.clear()
    for i in lista:
        i = (i[0], i[1], str("%.2f" % i[2]) + "€")
        piss.listSelServicios.append(i)

def cargarCamareros():
    """
    Al iniciarse el programa carga todos los camareros en la lista de camareros.
    """
    piss.curRestaurante.execute("select idCamarero from Camareros")
    lista = piss.curRestaurante.fetchall()
    piss.listCamareros.clear()
    for i in lista:
        piss.listCamareros.append(i)

def cargarMesas():
    """
    Al iniciarse el programa carga todas las mesas en la lista de mesas.
    """
    piss.curRestaurante.execute("select idMesa from Mesas")
    lista = piss.curRestaurante.fetchall()
    piss.listMesas.clear()
    for i in lista:
        piss.listMesas.append(i)


def cargarProvincias():
    """
    Al iniciarse el programa carga todas las provincias en ambas listas de provincias.
    """
    try:
        piss.listProvincias.clear()
        piss.listProvincias2.clear()
        piss.curReverb.execute("select provincia from provincias")
        provincias = piss.curReverb.fetchall()
        for i in provincias:
            piss.listProvincias.append(i)
            piss.listProvincias2.append(i)
    except sqlite3.OperationalError as e:
        print(e)


def cargarFacturas():
    """
    Al iniciarse el programa carga todas las facturas en la lista de facturas.
    """
    piss.listFacturas.clear()
    piss.curRestaurante.execute("select * from Facturas")
    facturas = piss.curRestaurante.fetchall()
    for i in facturas:
        piss.listFacturas.append((i[0], i[1], i[2], i[3], i[4], i[5], "%.2f" % i[6] + "€"));


def cargarClientes():
    """
    Al iniciarse el programa carga todlos los clientes en la lista de clientes.
    """
    piss.listClientes.clear()
    piss.curRestaurante.execute("select * from Clientes")
    clientes = piss.curRestaurante.fetchall()
    for i in clientes:
        piss.listClientes.append(i)


def cargarMunicipios(widget):
    """
    Evento que se lanza al elegir una provincia en el combo de provincias de la pestaña factura.
    """
    piss.listMunicipios.clear()
    piss.curReverb.execute("select municipio from municipios where provincia_id = " + str(piss.cmbProvincia.get_active() + 1) + "")
    municipios = piss.curReverb.fetchall()
    for i in municipios:
        piss.listMunicipios.append(i)


def cargarMunicipios2(widget):
    """
    Evento que se lanza al elegir una provincia en el combo de provincias del gestor de facturas.
    """
    piss.listMunicipios2.clear()
    piss.curReverb.execute(
        "select municipio from municipios where provincia_id = " + str(piss.cmbProvinciaAdm.get_active() + 1) + "")
    municipios = piss.curReverb.fetchall()
    for i in municipios:
        piss.listMunicipios2.append(i)


def cargarDatos(posicion):
    """
    Metodo que carga los datos de la mesa almacenados en el objeto correspondiente en la pestaña de factura.
    """
    piss.treeComandas.set_model(piss.listas[posicion])
    piss.treeComandas.show()
    piss.etDni.set_text(piss.mesas[posicion].dni)
    piss.etNombre.set_text(piss.mesas[posicion].nombre)
    piss.etApellidos.set_text(piss.mesas[posicion].apellidos)
    piss.etDireccion.set_text(piss.mesas[posicion].direccion)
    piss.cmbProvincia.set_active(piss.mesas[posicion].provincia)
    piss.cmbCiudad.set_active(piss.mesas[posicion].ciudad)
    piss.lblTotal.set_text(str(piss.mesas[posicion].total))


#EOF