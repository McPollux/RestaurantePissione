#from Restaurante.declaraciones import piss import --- Redundante ya que ya es importando en Restaurante.cargas
from Restaurante.facturas import factura
from Restaurante.cargas import *
import datetime


def guardarDatos():
    posicion = int(piss.lblMesa.get_text())
    piss.mesas[posicion].dni = piss.etDni.get_text()
    piss.mesas[posicion].nombre = piss.etNombre.get_text()
    piss.mesas[posicion].apellidos = piss.etApellidos.get_text()
    piss.mesas[posicion].direccion = piss.etDireccion.get_text()
    piss.mesas[posicion].provincia = piss.cmbProvincia.get_active()
    piss.mesas[posicion].ciudad = piss.cmbCiudad.get_active()
    piss.mesas[posicion].total = piss.lblTotal.get_text()

    vaciarFactura()


def abrirFactura(data, widget):

    piss.lblTotal.set_text("0")
    if widget == piss.btnMesa1:
        piss.lblMesa.set_text("1")
        cargarDatos(1)
    elif widget == piss.btnMesa2:
        piss.lblMesa.set_text("2")
        cargarDatos(2)
    elif widget == piss.btnMesa3:
        piss.lblMesa.set_text("3")
        cargarDatos(3)
    elif widget == piss.btnMesa4:
        piss.lblMesa.set_text("4")
        cargarDatos(4)
    elif widget == piss.btnMesa5:
        piss.lblMesa.set_text("5")
        cargarDatos(5)
    elif widget == piss.btnMesa6:
        piss.lblMesa.set_text("6")
        cargarDatos(6)
    elif widget == piss.btnMesa7:
        piss.lblMesa.set_text("7")
        cargarDatos(7)
    elif widget == piss.btnMesa8:
        piss.lblMesa.set_text("8")
        cargarDatos(8)

    piss.lblCamarero.set_text("Jordi Auxiliar")
    now = datetime.datetime.now()
    piss.lblFecha.set_text(str(now.day) + "/" + str(now.month) + "/" + str(now.year))

    piss.gbFactura.show()

    piss.notebook.set_current_page(1)


def buscarCliente(data, widget, data2=None):
    piss.booleanCliente = False
    piss.curRestaurante.execute("select * from Clientes")
    clientes = piss.curRestaurante.fetchall()
    for i in clientes:
        if piss.etDni.get_text() == i[0]:
            piss.etNombre.set_text(i[1])
            piss.etApellidos.set_text(i[2])
            piss.etDireccion.set_text(i[3])
            piss.cmbProvincia.set_active(idProvincia(i[4]))
            piss.cmbCiudad.set_active(idCiudad(i[5]))
            piss.booleanCliente = True


def idProvincia(nombre):
    piss.curReverb.execute("select id, provincia from provincias")
    provincias = piss.curReverb.fetchall()
    for i in provincias:
        if i[1] == nombre:
            return int(i[0] -1)


def idCiudad(nombre):
    cont = 0
    for i in piss.listMunicipios:
        if i[0] == nombre:
            return cont
        cont += 1


def anhadirComanda(data, widget):
    b = False

    seleccion = piss.treeSelServicios.get_selection()
    (tm, ti) = seleccion.get_selected()
    id = tm.get_value(ti, 0)
    precio = float([tm.get_value(ti, 2)[0:-1]][0])
    piss.lblTotal.set_text("%.2f" % (float(piss.lblTotal.get_text()) + precio))
    listaComandas = piss.listas[int(piss.lblMesa.get_text())]
    for i in range(len(listaComandas)):
        if id == listaComandas[i][0]:
            listaComandas[i][2] += 1
            listaComandas[i][3] = "%.2f" % (precio * listaComandas[i][2]) + "€"
            b = True
            break

    if not b:
        lista = (id, "%.2f" % precio + "€", 1,
                 "%.2f" % precio + "€")  # Precio sacado de la tabla de servicios, extraido el campo "€" y formateado para tener solo 2 decimales
        listaComandas.append(lista)


def eliminarComanda(self, widget):

    seleccion = self.treeComandas.get_selection()
    (tm, ti) = seleccion.get_selected()
    if ti is not None:
        precioComanda = float([tm.get_value(ti, 3)[0:-1]][0])
        self.lblTotal.set_text("%.2f" % (float(self.lblTotal.get_text()) - precioComanda))
        tm.remove(ti)


def imprimir(data, widget):

    piss.lblError.set_text("")

    if piss.etDni.get_text() == "":
        piss.lblError.set_text("El campo de DNI no puede estar vacio")
        return

    if piss.etNombre.get_text() == "":
        piss.lblError.set_text("El campo de nombre no puede estar vacio")
        return

    if piss.cmbProvincia.get_active() == -1:
        piss.lblError.set_text("El campo de provincia no puede estar vacio")
        return

    if piss.cmbCiudad.get_active() == -1:
        piss.lblError.set_text("El campo de ciudad no puede estar vacio")
        return

    if not piss.booleanCliente:
        altaClienteFac()

    altaFactura()
    vaciarFactura()
    piss.notebook.set_current_page(0)
    piss.gbFactura.hide()


def vaciarFactura():
    piss.etDni.set_text("")
    piss.etDireccion.set_text("")
    piss.etNombre.set_text("")
    piss.etApellidos.set_text("")
    piss.cmbProvincia.set_active(-1)
    piss.cmbCiudad.set_active(-1)


def altaFactura():

    lista = (piss.etDni.get_text(), 1, int(piss.lblMesa.get_text()), datetime.datetime.now(),
             float(piss.lblTotal.get_text()))

    piss.curRestaurante.execute(
        "insert into facturas (dni, idCamarero, idMesa, fecha, total) values (?, ?, ?, ?, ?)", lista)
    piss.conexPissione.commit()
    cargarFacturas()

    # Ahora cogemos la factura de la base de datos
    piss.curRestaurante.execute("select max(idFactura) from facturas")
    id = piss.curRestaurante.fetchall()


    for i in piss.treeComandas.get_model():
        piss.curRestaurante.execute("insert into lineasFactura (idFactura, idServicio, cantidad) values (?, ?, ?)",
                                    (id[0][0], i[0], i[2]))

    piss.conexPissione.commit()

    factura(id[0][0])
    piss.lblError.set_text("")
    piss.lblTotal.set_text("0")
    piss.treeComandas.get_model().clear()


def altaClienteFac():
    tree_prov = piss.cmbProvincia.get_active_iter()
    tree_local = piss.cmbCiudad.get_active_iter()
    model = piss.cmbProvincia.get_model()
    prov = model[tree_prov][0]
    model = piss.cmbCiudad.get_model()
    localidad = model[tree_local][0]

    lista = (
        piss.etDni.get_text(), piss.etNombre.get_text(), piss.etApellidos.get_text(), piss.etDireccion.get_text(),
        prov,
        localidad)
    piss.curRestaurante.execute("insert into clientes values (?, ?, ?, ?, ?, ?)", lista)
    piss.conexPissione.commit()


def bajaFactura(data, widget):
    a = piss.treeFacturas.get_selection()
    (tm, ti) = a.get_selected()
    piss.curRestaurante.execute("delete from facturas where idFactura = \'" + str(tm.get_value(ti, 0)) + "\'")
    piss.conexPissione.commit()

    piss.listLineasFactura.clear()
    cargarFacturas()


def visualizarComandas(data, widget):  # Metodo que se lanza al clicar en una tupla de la tabla facturas
    piss.listLineasFactura.clear()
    a = piss.treeFacturas.get_selection()
    (tm, ti) = a.get_selected()
    if ti is not None:
        piss.curRestaurante.execute("select * from LineasFactura where idFactura = \'" + str(tm.get_value(ti, 0)) + "\'")
        lineasFactura = piss.curRestaurante.fetchall()

        for i in lineasFactura:
            piss.curRestaurante.execute("select nombre, precio from servicios where idServicio = \'" + str(i[2]) + "\'")
            nombrePrecio = piss.curRestaurante.fetchall()
            piss.listLineasFactura.append((i[0], i[3], nombrePrecio[0][0], "%.2f" % (nombrePrecio[0][1] * i[3]) + "€"))

        piss.etIdFactura.set_text(str(tm.get_value(ti, 0)))
        piss.etDni2.set_text(str(tm.get_value(ti, 1)))
        piss.etFecha.set_text(str(tm.get_value(ti, 4)))


def printPDF(self, widget):
    a = self.treeFacturas.get_selection()
    (tm, ti) = a.get_selected()
    factura(tm.get_value(ti, 0))

def desSelect(data, widget):
    piss.treeNoFuncional.unselect_all()