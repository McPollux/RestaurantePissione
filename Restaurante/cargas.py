from Restaurante.declaraciones import piss
import sqlite3

def cargarServicios(data, widget):
    piss.curRestaurante.execute("select * from Servicios")
    lista = piss.curRestaurante.fetchall()
    piss.listSelServicios.clear()
    for i in lista:
        i = (i[0], i[1], str("%.2f" % i[2]) + "€")
        piss.listSelServicios.append(i)

def cargarCamareros(data, widget):
    piss.curRestaurante.execute("select idCamarero from Camareros")
    lista = piss.curRestaurante.fetchall()
    piss.listCamareros.clear()
    for i in lista:
        piss.listCamareros.append(i)

def cargarMesas(data, widget):
    piss.curRestaurante.execute("select idMesa from Mesas")
    lista = piss.curRestaurante.fetchall()
    piss.listMesas.clear()
    for i in lista:
        piss.listMesas.append(i)

def cargarDatos(data, posicion):
    piss.treeComandas.set_model(piss.listas[posicion])
    piss.treeComandas.show()
    piss.etDni.set_text(piss.mesas[posicion].dni)
    piss.etNombre.set_text(piss.mesas[posicion].nombre)
    piss.etApellidos.set_text(piss.mesas[posicion].apellidos)
    piss.etDireccion.set_text(piss.mesas[posicion].direccion)
    piss.cmbProvincia.set_active(piss.mesas[posicion].provincia)
    piss.cmbCiudad.set_active(piss.mesas[posicion].ciudad)
    piss.lblTotal.set_text(str(piss.mesas[posicion].total))

def cargarProvincias():
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

def cargarMunicipios(data, widget):
    piss.listMunicipios.clear()
    piss.curReverb.execute("select municipio from municipios where provincia_id = " + str(piss.cmbProvincia.get_active() + 1) + "")
    municipios = piss.curReverb.fetchall()
    for i in municipios:
        piss.listMunicipios.append(i)

def cargarMunicipios2(data, widget):
    piss.listMunicipios2.clear()
    piss.curReverb.execute(
        "select municipio from municipios where provincia_id = " + str(piss.cmbProvinciaAdm.get_active() + 1) + "")
    municipios = piss.curReverb.fetchall()
    for i in municipios:
        piss.listMunicipios2.append(i)

def cargarFacturas():
    piss.listFacturas.clear()
    piss.curRestaurante.execute("select * from Facturas")
    facturas = piss.curRestaurante.fetchall()
    for i in facturas:
        piss.listFacturas.append((i[0], i[1], i[2], i[3], i[4], i[5], "%.2f" % i[6] + "€"));

def cargarClientes():
    piss.listClientes.clear()
    piss.curRestaurante.execute("select * from Clientes")
    clientes = piss.curRestaurante.fetchall()
    for i in clientes:
        piss.listClientes.append(i)

#EOF